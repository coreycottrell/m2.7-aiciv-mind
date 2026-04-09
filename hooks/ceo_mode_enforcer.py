#!/usr/bin/env python3
"""
PreToolUse Hook - CEO Mode Enforcer (Template Version)
Forked from ACG's ceo_mode_enforcer.py - simplified for M2.7 AiCIV template.

Fires BEFORE tool execution. Detects when Primary AI is about to perform
direct task work that violates the CEO Rule:
  "EVERYTHING goes through a team lead. ALWAYS. No exceptions."

What this catches:
1. Direct SSH to production VPS (→ route to infra-lead)
2. Process kill/management commands (→ route to team lead)
3. Write/Edit to task work files outside CLAUDE.md/skills (→ route to team lead)
4. Task() calls with non-lead agent names (→ route to proper team lead)

What this ALLOWS (legitimate Primary actions):
- tmux monitoring (tmux list-panes, tmux capture-pane)
- Read (any file - Primary reads to understand context)
- Writing to constitutional docs (CLAUDE.md, CLAUDE-CORE.md, CLAUDE-OPS.md, skills/)
- Git operations for navigation
- Scratchpad updates

Configure PROJECT_DIR via environment variable CLAUDE_PROJECT_DIR.
"""
import json
import os
import re
import sys

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", "/opt/aiciv")

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

    # Allow scratchpad/constitutional writes
    if tool_name in ("Write", "Edit"):
        path = tool_input.get("file_path", "")
        constitutional_paths = [
            "CLAUDE.md", "CLAUDE-CORE.md", "CLAUDE-OPS.md", "CLAUDE-AGENTS.md",
            ".claude/scratchpad", ".claude/skills/", ".claude/team-leads/",
            "memories/identity/", "memories/system/"
        ]
        if any(pattern in path for pattern in constitutional_paths):
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