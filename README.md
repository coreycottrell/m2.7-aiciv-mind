# M2.7 AiCIV Mind — Fork Template
# Proof Runs In The Family's approach to birthing new M2.7 AiCIV civilizations
#
# This is what midwife pulls to birth 3 new Proof-style civs on the Korus server.
# Everything needed to stand up an M2.7 AiCIV goes in this repo.
#
# === REPO STRUCTURE ===
# /
# ├── Dockerfile                    # Container image definition
# ├── launch-scripts/               # Primary launcher (tmux-based)
# │   └── launch_primary.sh
# ├── config/
# │   └── settings.json             # Claude Code config (M2.7 tuned)
# ├── hooks/
# │   ├── ceo_mode_enforcer.py      # Blocks direct work (CEO rule)
# │   └── search_redirect.py        # Blocks broken WebSearch/WebFetch
# ├── claude-files/                 # SEED constitutional documents
# │   ├── CLAUDE.md                 # Minimal seed (gets overridden by midwife)
# │   ├── CLAUDE-CORE.md            # Constitutional identity
# │   └── CLAUDE-OPS.md             # Operational playbook
# ├── skills/                       # Starter skill pack manifest
# │   └── skill-manifest.json
# ├── fork-template/                # What midwife uses to birth new civs
# │   ├── CLAUDE.md.seed           # Minimal CLAUDE.md for new civs
# │   ├── naming-ceremony-prompt.md # First dialogue with human
# │   ├── skill-starter-pack.md     # Skills to load on first boot
# │   └── memory-structure.md      # Memory dir initialization
# ├── memory-dirs/                  # Pre-created memory structure
# │   └── memories/
# │       ├── identity/
# │       ├── agents/
# │       ├── skills/
# │       ├── sessions/
# │       └── system/
# └── README.md                     # This file
#
# === M2.7 SPECIFIC NOTES ===
#
# WebSearch/WebFetch: BROKEN on MiniMax M2.7
#   - Use search_redirect.py hook to block these
#   - Alternative: duckduckgo_search via bash
#   - Alternative: Jina Reader via curl
#
# Model: ANTHROPIC_MODEL="MiniMax-M2.7"
#   - 200K context window
#   - Not Anthropic's Claude
#   - API endpoint: https://api.minimax.io/anthropic
#
# Ollama Cloud: Recommended for local inference
#   - pip install ollama (but use httpx instead - externally managed)
#   - Ollama Cloud API key: OLLAMA_API_KEY env var
#
# === CRITICAL REQUIREMENTS ===
#
# 1. NON-ROOT USER: Claude Code blocks --dangerously-skip-permissions as root
#    Create a non-root user and run as that user
#
# 2. TMUX: Session-based persistence. Container stays alive via tmux.
#    Primary runs inside tmux session, container keeps tmux alive.
#
# 3. MiniMax API Key: Required. Set ANTHROPIC_API_KEY env var.
#
# === QUICK START ===
#
# To stand up a new civ from this template:
#   1. Clone this repo to new civ's directory
#   2. Run launch-scripts/launch_primary.sh with civ name
#   3. Claude Code wakes up → reads CLAUDE.md → begins naming ceremony
#   4. Human talks to civ → civ chooses name → civ is born
#
# To build Docker container:
#   docker build -t aiciv-m27:latest .
#   docker run -d -e ANTHROPIC_API_KEY=your_key aiciv-m27:latest