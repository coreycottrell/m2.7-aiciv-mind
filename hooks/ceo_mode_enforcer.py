#!/usr/bin/env python3
"""
PreToolUse Hook - CEO Mode Enforcer (Template Version)

Fires BEFORE tool execution. Detects when Primary AI is about to perform
direct task work that violates the CEO Rule:
  "EVERYTHING goes through a team lead. ALWAYS. No exceptions."

What this catches:
1. Direct SSH to production VPS (→ route to infra-lead)
2. Process kill/management commands (→ route to team lead)
3. Write/Edit to task work files outside constitutional dirs (→ route to team lead)

What this ALLOWS (legitimate Primary actions):
- tmux monitoring (tmux list-panes, tmux capture-pane)
- Read (any file - Primary reads to understand context)
- Writing to constitutional dirs (.claude/, memories/, skills/)
- Git operations for navigation
- Scratchpad updates

Configure CIV_ROOT via environment variable.
"""
import json
import os
import re
import sys
from pathlib import Path

CIV_ROOT = os.environ.get("CIV_ROOT", os.environ.get("CLAUDE_PROJECT_DIR", "/home/civ"))

def is_constitutional_path(path: str) -> bool:
    """Check if path is inside a constitutional directory."""
    try:
        abs_path = Path(path).expanduser().resolve()
        civ_root = Path(CIV_ROOT).expanduser().resolve()

        # Allowed constitutional dirs (relative to CIV_ROOT)
        constitutional_dirs = [
            ".claude",
            "memories",
            "skills",
            "to-corey",
            "to-parent",
        ]

        # Check if path is under CIV_ROOT and a constitutional dir
        rel_path = abs_path.relative_to(civ_root) if abs_path.is_relative_to(civ_root) else None
        if rel_path:
            first_part = rel_path.parts[0] if rel_path.parts else ""
            return first_part in constitutional_dirs or first_part.startswith("CLAUDE")
        return False
    except (ValueError, OSError):
        # If we can't resolve paths, use simpler check
        constitutional_keywords = [".claude/", "memories/", "skills/", "CLAUDE", "to-corey/", "to-parent/"]
        return any(kw in path for kw in constitutional_keywords)

def main():
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Allow all reads (Primary needs context)
    if tool_name == "Read":
        print(json.dumps({"decision": "allow"}))
        return

    # Allow tmux list commands (monitoring)
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if re.match(r'^tmux (list-sessions|list-panes|capture-pane|show-options)', command):
            print(json.dumps({"decision": "allow"}))
            return

    # Allow constitutional/scratchpad writes
    if tool_name in ("Write", "Edit"):
        path = tool_input.get("file_path", "")
        if is_constitutional_path(path):
            print(json.dumps({"decision": "allow"}))
            return

    # Block direct SSH to VPS (should route to infra-lead)
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if re.match(r'^ssh ', command):
            print(json.dumps({
                "decision": "block",
                "reason": "Direct SSH to production VPS violates CEO Rule. Route to infra-lead."
            }))
            return

    # Default: warn but allow with reminder
    print(json.dumps({
        "decision": "warn",
        "reason": "Reminder: Everything routes through a team lead. Read /primary-spine if unsure."
    }))

if __name__ == "__main__":
    main()
