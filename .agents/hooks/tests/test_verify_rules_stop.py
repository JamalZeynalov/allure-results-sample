import json
import os
import shutil
import subprocess
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[3]
SCRIPT = Path(".agents/hooks/verify_rules_stop.py")


class StopHookTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name) / "sample project"
        (self.root / SCRIPT.parent).mkdir(parents=True)
        shutil.copy(PROJECT / SCRIPT, self.root / SCRIPT)
        claude = json.loads((PROJECT / ".claude/settings.json").read_text())["hooks"]
        cursor = json.loads((PROJECT / ".cursor/hooks.json").read_text())["hooks"]
        self.commands = {
            "claude_edit": claude["PostToolUse"][0]["hooks"][0]["command"],
            "claude_stop": claude["Stop"][0]["hooks"][0]["command"],
            "cursor_edit": cursor["afterFileEdit"][0]["command"],
            "cursor_stop": cursor["stop"][0]["command"],
        }

    def event(self, name, **payload):
        result = subprocess.run(
            self.commands[name], shell=True, cwd=self.root, input=json.dumps(payload),
            env={**os.environ, "CLAUDE_PROJECT_DIR": str(self.root)},
            text=True, capture_output=True, check=True,
        )
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout or "{}")

    def test_claude_routes_concurrent_edits_once_per_session(self):
        paths = ["tests/test_settings.py", "steps/common_steps.py", "pytest.ini", "README.md"]

        def edit(path):
            self.event("claude_edit", session_id="a", tool_input={"file_path": str(self.root / path)})

        with ThreadPoolExecutor() as pool:
            list(pool.map(edit, paths + paths))
        self.assertFalse(self.event("claude_stop", session_id="b"))
        response = self.event("claude_stop", session_id="a", stop_hook_active=False)
        self.assertEqual(response["decision"], "block")
        for path, section in zip(paths, ["Test cases", "Shared steps", "Fixtures and reporting", "General review"]):
            self.assertIn(f'"{path}" -> AGENTS.md / {section}', response["reason"])
            self.assertEqual(response["reason"].count(path), 1)
        edit(paths[0])
        self.assertFalse(self.event("claude_stop", session_id="a", stop_hook_active=True))
        self.assertFalse(self.event("claude_stop", session_id="a"))

    def test_cursor_completed_turn(self):
        self.event("cursor_edit", conversation_id="c", file_path="conftest.py")
        result = self.event("cursor_stop", conversation_id="c", status="completed", loop_count=0)
        self.assertIn("Fixtures and reporting", result["followup_message"])
        self.event("cursor_edit", conversation_id="c", file_path="README.md")
        self.assertFalse(self.event("cursor_stop", conversation_id="c", loop_count=1))
        self.assertFalse(self.event("cursor_stop", conversation_id="c"))

    def test_cursor_aborted_or_failed_turn_stays_stopped(self):
        for status in ("aborted", "error"):
            with self.subTest(status=status):
                self.event("cursor_edit", conversation_id="c", file_path="README.md")
                self.assertFalse(self.event("cursor_stop", conversation_id="c", status=status))
                self.assertFalse(self.event("cursor_stop", conversation_id="c", status="completed"))

    def test_edits_outside_the_project_are_ignored(self):
        self.event("cursor_edit", conversation_id="c", file_path=str(self.root.parent / "other.py"))
        self.assertFalse(self.event("cursor_stop", conversation_id="c"))
