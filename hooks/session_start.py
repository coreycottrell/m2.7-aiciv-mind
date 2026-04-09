#!/usr/bin/env python3
"""
SessionStart Hook — Initializes Session Ledger

Fires when Claude Code starts a new session. Creates session ledger file
for tracking work across the session lifetime.

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
    session_type = data.get("session_type", "startup")

    # Create session ledger directory
    sessions_dir = Path(PROJECT_DIR) / "memories" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)

    # Create current session ledger with timestamp
    now = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    ledger_path = sessions_dir / f"session-{now}.jsonl"

    # Initialize ledger
    ledger_data = {
        "session_id": now,
        "session_type": session_type,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "tools_used": [],
        "tasks_completed": []
    }

    with open(ledger_path, "w") as f:
        f.write(json.dumps(ledger_data) + "\n")

    # Always allow session to start
    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
