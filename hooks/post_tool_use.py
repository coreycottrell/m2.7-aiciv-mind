#!/usr/bin/env python3
"""
PostToolUse Hook — Tool Usage Logger

Fires AFTER each tool execution. Logs tool usage to session ledger
for tracking what was done during the session.

Configure PROJECT_DIR via environment variable CLAUDE_PROJECT_DIR.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", "/home/civ/civ-data")


def main():
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    tool_result = data.get("tool_result", {})
    error = data.get("error", None)

    # Get current session ledger
    sessions_dir = Path(PROJECT_DIR) / "memories" / "sessions"
    if sessions_dir.exists():
        # Find most recent session ledger
        ledgers = sorted(sessions_dir.glob("session-*.jsonl"), reverse=True)
        if ledgers:
            ledger_path = ledgers[0]
            # Append tool usage entry
            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "tool": tool_name,
                "error": error
            }
            with open(ledger_path, "a") as f:
                f.write(json.dumps(entry) + "\n")

    # Always allow (post-tool hooks can't block)
    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
