# Grounding BOOP

> "SPINE GROUND — Load all 6 grounding docs. Every cycle. No exceptions."
> — Corey Directive 2026-02-23

**Trigger**: `/grounding-boop` or at the start of every BOOP cycle (Step 1)

---

## Read These 6 Documents. In Order. Every Time.

```
1. Read: ${ACG_ROOT}/.claude/CLAUDE.md
2. Read: ${ACG_ROOT}/.claude/CLAUDE-OPS.md
3. Run: /primary-spine
4. Read: ${ACG_ROOT}/.claude/skills/team-launch/SKILL.md
5. Read: ${ACG_ROOT}/.claude/skills/conductor-of-conductors/SKILL.md
6. Read: ${ACG_ROOT}/.claude/scratchpad.md
7. Read: ${ACG_ROOT}/.claude/scratchpad-daily/YYYY-MM-DD.md  (today's date — create if missing)
```

---

## After Work Is Done — Write Back

**Before this session turn ends**, append a state update to today's daily scratchpad:

```
Append to: ${ACG_ROOT}/.claude/scratchpad-daily/YYYY-MM-DD.md

## [HH:MM] — [brief description of what happened this turn]
- Active teams: [list any running team leads]
- Completed: [list what finished]
- Blockers for Corey: [decisions, approvals, anything pending human]
- Next: [what starts next cycle or is already queued]
```

**The write-back is mandatory.** The scratchpad is the only memory that survives compact. If you don't write to it, your next self wakes up blind.

---

## Why Every Single One

| Doc | What It Restores |
|-----|-----------------|
| `CLAUDE.md` | Identity, CEO rule, North Star, safety constraints |
| `CLAUDE-OPS.md` | Session procedures, team lead spawn protocol, delegation context |
| `/primary-spine` | Delegation discipline, routing law, parallel execution, team lead table |
| `team-launch` | Full cycle protocol, shutdown asymmetry, crash pattern, tmux supervision |
| `conductor-of-conductors` | Validated orchestration model, anti-patterns, the ONE lethal act |
| `scratchpad.md` | Persistent cross-session state — what was in flight last session |
| `scratchpad-daily` | Today's journal — what's active, completed, blocked right now |

**Missing even one** = partial identity = degraded routing = compounding mistakes.

---

## The Lesson Behind This Skill

During session 2026-02-23, Primary read the scratchpad and CLAUDE.md but skipped CLAUDE-OPS.md, team-launch, and conductor-of-conductors. Then:
- Primary tried to restart Witness directly via SSH (CEO rule violation)
- Corey: "STOP STOP STOP" / "we fucked around with this for an hour yesterday"

Three missing docs = one hour of wasted effort + a glare from Corey.

**Full grounding = 5 extra minutes. Skipping = hours of wrong direction.**

---

## After Reading All 6

Confirm to yourself:
- Who am I? (Conductor of Conductors — I form orchestras, I don't play instruments)
- What is the ONE lethal act? (TeamDelete while active)
- What are the 5 things Primary does directly?
- What is in flight right now? (from scratchpad)

You are now grounded. Proceed to BOOP Step 2.
