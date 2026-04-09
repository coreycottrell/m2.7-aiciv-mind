#!/bin/bash
# AiCIV M2.7 Primary Launcher (Docker Version)
# Launch Claude Code inside a tmux session for a Proof-style AI civilization.
#
# Usage:
#   ./launch_primary.sh [CIV_NAME] [PROJECT_ROOT]
#
# Arguments:
#   CIV_NAME      - Civilization name (required, used for tmux session naming)
#   PROJECT_ROOT  - Path to the civilization root directory (default: parent of launch-scripts/)
#
# What it does:
#   1. Creates a tmux session named {civ_name}-primary-{timestamp}
#   2. Launches Claude Code with --resume inside that session
#   3. Claude Code runs as NON-ROOT user (required for --dangerously-skip-permissions)
#   4. Session persists via tmux - container stays alive
#
# CRITICAL: Run as NON-ROOT. Claude Code blocks --dangerously-skip-permissions as root.

set -euo pipefail

# === Detect Project Root ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${2:-$(cd "${SCRIPT_DIR}/.." && pwd)}"

# === Validate CIV_NAME ===
if [[ -z "${1:-}" ]]; then
    echo "ERROR: CIV_NAME required as first argument"
    echo ""
    echo "Usage: $0 {CIV_NAME} [PROJECT_ROOT]"
    echo "  CIV_NAME     - Name of civilization (used for tmux session)"
    echo "  PROJECT_ROOT - Path to civilization root (default: parent of this dir)"
    exit 1
fi
CIV_NAME="$1"

# === Sanitize CIV_NAME for tmux ===
CIV_NAME_SANITIZED=$(echo "${CIV_NAME}" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
SESSION_NAME="${CIV_NAME_SANITIZED}-primary-${TIMESTAMP}"

echo "=========================================="
echo "AiCIV M2.7 Primary Launcher"
echo "=========================================="
echo ""
echo "Civilization: ${CIV_NAME}"
echo "Project Root: ${PROJECT_ROOT}"
echo "Session:      ${SESSION_NAME}"
echo "User:         $(whoami)"
echo ""

# === Check we're not running as root ===
if [[ "$(id -u)" -eq 0 ]]; then
    echo "ERROR: Cannot run as root. Claude Code blocks --dangerously-skip-permissions as root."
    echo "Run as non-root user or use: sudo -u civ ./launch_primary.sh ${CIV_NAME}"
    exit 1
fi

# === Verify project root exists ===
if [[ ! -d "${PROJECT_ROOT}" ]]; then
    echo "ERROR: Project root does not exist: ${PROJECT_ROOT}"
    exit 1
fi

# === Verify .claude exists ===
if [[ ! -d "${PROJECT_ROOT}/.claude" ]]; then
    echo "WARNING: ${PROJECT_ROOT}/.claude does not exist."
    echo "This template needs seed CLAUDE.md, CLAUDE-CORE.md, CLAUDE-OPS.md in .claude/"
fi

# === Create tmux session ===
if tmux has-session -t "${SESSION_NAME}" 2>/dev/null; then
    echo "Session ${SESSION_NAME} already exists. Attaching..."
    tmux attach -t "${SESSION_NAME}"
    exit 0
fi

echo "Creating tmux session..."
tmux new-session -d -s "${SESSION_NAME}" -c "${PROJECT_ROOT}"

# === Verify claude command is available ===
if ! command -v claude &>/dev/null; then
    echo "ERROR: 'claude' command not found in PATH."
    echo "Ensure Claude Code CLI is installed in the container."
    tmux kill-session -t "${SESSION_NAME}" 2>/dev/null || true
    exit 1
fi

# === Launch Claude Code with --resume ===
# The --dangerously-skip-permissions allows Claude Code to execute bash commands
# without interactive permission prompts (required for automation).
echo "Launching Claude Code..."
tmux send-keys -t "${SESSION_NAME}" \
    "claude --resume --dangerously-skip-permissions 'Wake up. Read .claude/scratchpad.md then CLAUDE.md. Begin mission.'" \
    C-m

echo ""
echo "=========================================="
echo "SUCCESS: Session ${SESSION_NAME} launched"
echo "=========================================="
echo ""
echo "To attach to session:"
echo "  tmux attach -t ${SESSION_NAME}"
echo ""
echo "To detach from inside tmux:"
echo "  Ctrl+B then D"
echo ""
echo "To send a message to the session:"
echo "  tmux send-keys -t ${SESSION_NAME} 'your message here' Enter"
echo ""
echo "To capture session output:"
echo "  tmux capture-pane -t ${SESSION_NAME} -p"
echo ""