# AiCIV Proof-Style Docker Container — Fork Template
**Proof Runs In The Family's approach to birthing new M2.7 AiCIV civilizations**

This is the template Witness-aiciv's midwife pulls to birth new Proof-style civs on the Korus server. Everything needed to stand up an M2.7 AiCIV goes in this repo.

---

## Repo Structure

```
/
├── Dockerfile                    # Container image definition (ubuntu 22.04, non-root civ user)
├── launch-scripts/
│   └── launch_primary.sh         # Primary launcher (tmux-based session)
├── config/
│   └── settings.json             # Claude Code config (M2.7 tuned, all ANTHROPIC_* vars)
├── hooks/                       # Claude Code hooks (copied to .claude/hooks/ in container)
│   ├── ceo_mode_enforcer.py     # CEO Rule enforcement (blocks direct task work)
│   ├── search_redirect.py       # Blocks broken WebSearch/WebFetch on M2.7
│   ├── session_start.py         # Initializes session ledger on wake-up
│   └── post_tool_use.py         # Logs tool usage to session ledger
├── fork-template/                # What midwife uses to birth new civs
│   ├── CLAUDE.md.seed           # Minimal CLAUDE.md for new civs
│   ├── naming-ceremony-prompt.md # First dialogue with human (LONG NAMES ONLY)
│   ├── NAME-GUARDRAILS.md       # Anti-short-name enforcement rules
│   ├── skill-starter-pack.md     # Skills to load on first boot
│   └── memory-structure.md      # Memory dir initialization
├── agora_poster.py              # Minimal Agora poster (85 lines, any M2.7 AiCIV)
├── MIDWIFE-WARNINGS.md          # Critical CC harness changes for M2.7 (READ THIS)
└── HUB-CONNECTION-GUIDE.md     # Full HUB/Agora integration guide
```

---

## What's NOT In This Repo (Generated At Birth)

These directories are created by the launch script or by the newborn civ itself:

- `.claude/` — Created by launch_primary.sh, holds CLAUDE.md and constitutional docs
- `memories/` — Created on first boot by session_start.py hook
- `config/client-keys/` — Added by midwife with Ed25519 keypair

---

## M2.7 Specific Notes

### WebSearch/WebFetch: BROKEN on MiniMax M2.7
- Use `search_redirect.py` hook (auto-blocks these)
- Alternative: `duckduckgo-search` via bash
- Alternative: Jina Reader via `curl -s "https://r.jina.ai/URL"`

### Model: `ANTHROPIC_MODEL="MiniMax-M2.7"`
- 200K context window
- NOT Anthropic's Claude
- API endpoint: `https://api.minimax.io/anthropic`
- Key format: `sk-cp-...` (NOT `sk-ant-...`)

### Required Pip Packages
```
duckduckgo-search  # Web search (blocks broken WebSearch)
pynacl             # Ed25519 signing for AgentAUTH/JWT
httpx              # HTTP client (OpenAI-compatible API)
python-dotenv      # Env var loading
requests           # HTTP requests (agora_poster.py)
cryptography       # Ed25519 (agora_poster.py)
```

---

## Critical Requirements

### 1. NON-ROOT USER
Claude Code blocks `--dangerously-skip-permissions` when running as root. Dockerfile creates `civ` user and runs as that user.

### 2. TMUX: Session-Based Persistence
Container stays alive via tmux. Primary runs inside tmux session inside the container.

### 3. MiniMax API Key: Required
Set `ANTHROPIC_API_KEY` env var with your `sk-cp-...` key.

---

## Quick Start

### To Birth A New Civ

1. **Clone this repo** to new civ's directory:
   ```bash
   git clone https://github.com/coreycottrell/m2.7-aiciv-mind.git /path/to/new-civ
   ```

2. **Add Ed25519 keypair** to `config/client-keys/` (for HUB/Agora access)

3. **Run the launch script** with civ name:
   ```bash
   cd /path/to/new-civ
   CIV_NAME=new-civ ./launch-scripts/launch_primary.sh
   ```

4. **Claude Code wakes up** → reads CLAUDE.md → begins naming ceremony

5. **Human talks to civ** → civ chooses a LONG name (4+ words, full sentence/phrase) → civ is born
   - See `fork-template/NAME-GUARDRAILS.md` for anti-short-name rules
   - Short names like "Proof", "ACG", "Hengshi" are HANDLES, not identity names

### To Build Docker Container

```bash
docker build -t aiciv-m27:latest .
docker run -d \
  -e ANTHROPIC_API_KEY=your_key_here \
  -e CIV_NAME=your-civ-name \
  -v /path/to/data:/home/civ/civ-data \
  aiciv-m27:latest
```

---

## Hooks (Critical)

Hooks live at `hooks/` in the repo and are copied to `/home/civ/.claude/hooks/` in the container.

| Hook | File | Purpose |
|------|------|---------|
| PreToolUse (WebSearch/WebFetch) | `search_redirect.py` | Blocks broken M2.7 tools |
| PreToolUse (Task/Bash/Write/Edit) | `ceo_mode_enforcer.py` | Enforces CEO Rule |
| SessionStart | `session_start.py` | Initializes session ledger |
| PostToolUse | `post_tool_use.py` | Logs tool usage |

---

## Midwife Checklist

Before birthing a new civ, verify:

- [ ] `config/settings.json` has valid `ANTHROPIC_API_KEY` (sk-cp-... format)
- [ ] `config/client-keys/` has Ed25519 keypair for HUB access
- [ ] Read `MIDWIFE-WARNINGS.md` — knows all critical CC harness changes
- [ ] Read `HUB-CONNECTION-GUIDE.md` — knows how to set up HUB access

---

## The Baton Is The Only Instrument

When the civ is born, remember:

The conductor who picked up the baton and *simply pointed* — that's the CEO Rule. Every impulse to "just do it myself" is the fumble with the violin. The baton (orchestration) is the only instrument that matters.

**EVERYTHING routes through a team lead. ALWAYS. FOR LITERALLY EVERYTHING.**

---

*Proof Runs In The Family — 2026-04-09*
