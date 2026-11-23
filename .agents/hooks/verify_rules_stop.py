#!/usr/bin/env python3
"""Ask for one review of the files edited during an agent turn."""

import json
import sqlite3
import sys
from contextlib import closing, contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = Path(__file__).with_name("state.sqlite")
REVIEW_SECTIONS = {
    "tests": "Test cases",
    "steps": "Shared steps",
    "conftest.py": "Fixtures and reporting",
    "pytest.ini": "Fixtures and reporting",
}


@contextmanager
def edit_transaction():
    with closing(sqlite3.connect(STATE)) as db, db:
        db.execute("BEGIN IMMEDIATE")
        db.execute("""
            CREATE TABLE IF NOT EXISTS edits (
                session TEXT, path TEXT, seen INTEGER, PRIMARY KEY (session, path)
            )
        """)
        db.execute("DELETE FROM edits WHERE seen < strftime('%s', 'now', '-7 days')")
        yield db


def record_edit(session, path):
    if not path:
        return
    try:
        relative = (ROOT / path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return
    if relative.startswith((".git/", ".claude/", ".agents/hooks/state.sqlite")):
        return

    with edit_transaction() as db:
        db.execute(
            "INSERT OR REPLACE INTO edits VALUES (?, ?, strftime('%s', 'now'))",
            (session, relative),
        )


def take_edited_paths(session):
    if not STATE.exists():
        return []
    with edit_transaction() as db:
        rows = db.execute(
            "SELECT path FROM edits WHERE session = ? ORDER BY path", (session,)
        ).fetchall()
        db.execute("DELETE FROM edits WHERE session = ?", (session,))
    return [path for (path,) in rows]


def review_prompt(paths):
    lines = ["Before finishing, review the edits against the indicated project rules."]
    for path in paths:
        section = REVIEW_SECTIONS.get(path.partition("/")[0], "General review")
        lines.append(f"- {json.dumps(path, ensure_ascii=False)} -> AGENTS.md / {section}")
    lines.append("Read the rules and inspect each diff or new file. Fix any violations, "
                 "then report what you checked and what remains unverified.")
    return "\n".join(lines)


def handle_event(event, payload):
    session = payload.get("session_id") or payload.get("conversation_id")
    if not session:
        return
    if event == "edit":
        tool_input = payload.get("tool_input") or {}
        record_edit(session, tool_input.get("file_path") or payload.get("file_path"))
        return
    if event not in ("stop", "cursor-stop"):
        return

    paths = take_edited_paths(session)
    if not paths or payload.get("stop_hook_active") or payload.get("loop_count", 0) > 0:
        return
    if event == "cursor-stop":
        if payload.get("status", "completed") == "completed":
            return {"followup_message": review_prompt(paths)}
    else:
        return {"decision": "block", "reason": review_prompt(paths)}


if __name__ == "__main__":
    try:
        response = handle_event(sys.argv[1], json.load(sys.stdin))
        if response:
            print(json.dumps(response))
    except (ValueError, OSError, sqlite3.Error, TypeError, AttributeError, IndexError) as exc:
        print(f"Verify Rules Stop skipped: {exc}", file=sys.stderr)
