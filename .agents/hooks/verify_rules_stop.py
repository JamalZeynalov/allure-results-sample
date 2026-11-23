#!/usr/bin/env python3
"""Record agent edits and request one change-specific review at stop."""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = Path(__file__).with_name("state.sqlite")
ROUTES = {
    "tests": "AGENTS.md / Test cases",
    "steps": "AGENTS.md / Shared steps",
    "conftest.py": "AGENTS.md / Fixtures and reporting",
    "pytest.ini": "AGENTS.md / Fixtures and reporting",
}


def run(event, payload):
    session = payload.get("session_id") or payload.get("conversation_id")
    if not session:
        return
    if event == "edit":
        path = (payload.get("tool_input") or {}).get("file_path") or payload.get("file_path")
        if not path:
            return
        try:
            relative = (ROOT / path).resolve().relative_to(ROOT).as_posix()
        except ValueError:
            return
        if relative.startswith((".git/", ".claude/", ".agents/hooks/state.sqlite")):
            return
    elif not STATE.exists():
        return

    with sqlite3.connect(STATE, isolation_level=None) as db:
        db.execute("BEGIN IMMEDIATE")
        db.execute("CREATE TABLE IF NOT EXISTS edits (session TEXT, path TEXT, "
                   "seen INTEGER, PRIMARY KEY(session, path))")
        db.execute("DELETE FROM edits WHERE seen < strftime('%s','now','-7 days')")
        if event == "edit":
            db.execute("INSERT OR REPLACE INTO edits VALUES (?, ?, strftime('%s','now'))",
                       (session, relative))
            return
        paths = [row[0] for row in db.execute(
            "SELECT path FROM edits WHERE session = ? ORDER BY path", (session,))]
        db.execute("DELETE FROM edits WHERE session = ?", (session,))

    if not paths or payload.get("stop_hook_active") or payload.get("loop_count", 0) > 0:
        return
    lines = ["Before finishing, review the edits against the indicated project rules."]
    for path in paths:
        rule = ROUTES.get(path.split("/")[0], "AGENTS.md / General review")
        lines.append(f"- {json.dumps(path, ensure_ascii=False)} -> {rule}")
    lines.append("Read the rules and inspect each diff or new file. Fix any violations, "
                 "then report what you checked and what remains unverified.")
    message = "\n".join(lines)
    if event == "cursor-stop":
        print(json.dumps({"followup_message": message}))
    else:
        print(json.dumps({"decision": "block", "reason": message}))


if __name__ == "__main__":
    try:
        run(sys.argv[1], json.load(sys.stdin))
    except (ValueError, OSError, sqlite3.Error, TypeError, AttributeError, IndexError) as exc:
        print(f"Verify Rules Stop skipped: {exc}", file=sys.stderr)
