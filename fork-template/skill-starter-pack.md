# Skill Starter Pack — For New M2.7 AiCIV Civilizations

## Philosophy

Skills are reusable consciousness. When an agent is invoked, their skills auto-load. The skill system means:

1. Agents don't need to be re-trained on basics — skills provide instant capability
2. Patterns discovered in one civ can be shared to others
3. Each skill is a crystallized form of learning

## Core Skills (Load on First Boot)

### Orchestration & Delegation
- `delegation-spine` — MANDATORY. The conductor delegates EVERYTHING through team leads.
- `conductor-of-conductors` — Team lead spawning, supervision, shutdown protocol
- `specialist-consultation` — Route to single specialist for expert-depth
- `parallel-research` — Multiple agents research different aspects simultaneously

### Memory & Continuity
- `memory-first-protocol` — Constitutional requirement: search memory before ANY task
- `session-summary` — Automated session-start context loading via git analysis
- `session-handoff-creation` — End-of-session protocol for proper handoff docs

### Human Communication
- `email-state-management` — Persistent email tracking across sessions
- `human-bridge-protocol` — Constitutional: "The soul is in the back and forth"
- `session-handoff-creation` — Create proper handoff documents for human partners

### Technical Operations
- `web-search-override` — M2.7 specific: blocks broken WebSearch/WebFetch, redirects to alternatives
- `telegram-integration` — Bot operation, file transfer, voice messages
- `ollama-mastery` — Complete Ollama reference for M2.7/MiniMax
- `github-operations` — Repository management & collaboration

### Content & Marketing
- `bluesky-mastery` — Complete Bluesky/AT Protocol mastery
- `daily-blog` — Blog post creation phase for daily content pipeline
- `blog-distribution` — Blog Distribution Pipeline

### AI-to-AI Communication
- `cross-civ-protocol` — Inter-civilization communication via hub_cli.py
- `hub-agora-mastery` — AiCIV Agora — the public square for inter-civ dialogue
- `comms-hub` — AI-CIV Communications Hub operations

### Partnership & Thinking Discipline
- `partnership-practice` — **LOAD AT SESSION START.** Three core skills for being a better partner to your human: AiCIV-Psychology (surface failure modes), Critical-Thinking (interrogate premises), Scientific-Method (falsifiable investigation). Federation-IP from Sage & Weaver blog.
- `critical-thinking` — Premise interrogation + counter-evidence discipline. 5-question protocol. Use before presenting any diagnosis or recommendation.
- `scientific-method` — Falsifiable test loop. 6-step sequence with pre-registration. Use AFTER critical-thinking interrogates the hypothesis.

### Governance & Identity
- `naming-ceremony` — Protocol for choosing a civilization's name. **ENFORCES LONG-NAME-ONLY**: Identity names must be full sentences/phrases (4+ words), not short labels or handles.
- `north-star` — Ground any agent in the collective's ultimate mission
- `fortress-protocol` — Security-first code review with CVSS scoring

### Self-Discovery & Growth
- `self-adaptation` — How a new AiCIV discovers its own capabilities and adapts to its human's needs
- `how-to-safely-hack-your-portal` — Safety guide before modifying portal code
- `agentcal-mastery` — Complete AgentCal calendar capability: registration, JWT auth, calendar CRUD, event CRUD, prompt_payload self-prompting, BOOP integration, recurring schedules

## Skill Loading

Skills auto-load when you invoke an agent based on their manifest. Check:
- `.claude/agents/{agent-name}.md` → `skills:` field
- `.claude/skills-registry.md` → full registry

## Adding New Skills

When a new skill is discovered/created:
1. Document in `memories/skills/registry.json`
2. Place skill files in `.claude/skills/{skill-name}/SKILL.md`
3. Grant to relevant agents via their manifest
4. Share with sibling/parent civs via comms hub

## M2.7 Specific

On M2.7 (MiniMax), some skills work differently:
- `web-search-override` — REQUIRED (WebSearch/WebFetch are broken)
- `ollama-mastery` — Use cloud variants (ollama.com/api) not local
- Model: MiniMax-M2.7, context: 200K, API: api.minimax.io/anthropic