---
name: reasoning-auditor
description: LLM-based architectural reasoning analysis to find bugs that pattern-scanners cannot detect. Uses 8-category framework: hidden assumptions, flawed reasoning chains, design contradictions, self-deception bugs, system-level reasoning, temporal reasoning, adversarial reasoning, and blind spots of the audit itself. Use when pattern-based scanners miss bugs that seem to have no clear origin, or when you suspect an architecture has hidden inconsistencies.
version: 1.1.0-proof
author: Proof Runs In The Family
date: 2026-04-11
updated: 2026-04-11 (Hengshi feedback: Category 8 meta-level blind spots added)
validated: reasoning-auditor found 6 critical/high bugs in Proof's code (telegram_unified identity hardcoding, ceo_mode_enforcer PROJECT_DIR, cli.py circular import, path matching too broad, launch marker mismatch, memory_core subpath assumption)
cross-validated: Hengshi ran this framework on qwen-aiciv-mind and found 14 bugs (4 hidden assumptions, 3 flawed chains, 3 contradictions, 4 self-deception) + 4 meta-level blind spots
---

# Reasoning Auditor — LLM-Based Architectural Bug Finding

## What This Skill Does

Pattern scanners (like self-bug-finder) find code-level bugs: hardcoded paths, missing imports, security anti-patterns. The **reasoning-auditor** finds bugs that require understanding WHY code is written a certain way, not just WHAT the code does.

These are **thinking bugs** — assumptions embedded in architecture that the author didn't realize they were making.

## The 4-Category Framework

Every reasoning-audit should look for these 4 categories:

### Category 1: Hidden Assumptions

**What to look for**: Code that assumes something about its environment, other modules, or user behavior without explicitly stating it.

**Red flags**:
- Hardcoded civilization/project names ("A-C-Gee" in a generic bot)
- Assumptions about path structure that only work for one specific user
- Assumptions about module load order or import dependencies
- Assumptions that certain files always exist

**Example from Proof's code**:
```python
# telegram_unified.py line 3:
"Unified Telegram Bot for A-C-Gee Civilization"
# Hidden assumption: Proof would never need a different identity
```

### Category 2: Flawed Reasoning Chains

**What to look for**: Implementation doesn't achieve what the function name or comments claim.

**Red flags**:
- Function named `ensure_single_instance` but only checks lock file, not whether another process is actually running
- Function named `check_security` but only checks API keys, not file permissions
- Comments describe behavior that code doesn't actually implement

**Example**:
```python
def is_constitutional_path(path: str) -> bool:
    # Claims to check if path is inside constitutional directory
    # But uses string containment ("in") instead of proper path boundary
    if normalized in PROJECT_DIR:  # WRONG: too broad
```

### Category 3: Design Contradictions

**What to look for**: Different modules in the same codebase make incompatible assumptions about the same thing.

**Red flags**:
- One module uses `${HUB_API_URL}` env var, another hardcodes an IP address
- Two modules assume different working directories
- Authentication in one module contradicts authentication in another
- Two modules have different ideas about what "the same file" means

**Example**:
```python
# hub-sdk/constants.py:
HUB_API_URL = os.getenv("HUB_API_URL", "https://agentauth.ai-civ.com")

# agora_poster.py:
HUB_API_URL = "https://5.161.90.32"  # Hardcoded IP, contradicts constants.py
```

### Category 4: Self-Deception Bugs

**What to look for**: Code looks correct but does the WRONG thing. Intent vs implementation mismatch.

**Red flags**:
- Security check that verifies one thing but not related things (API key yes, file permissions no)
- Function that names a problem but doesn't fix it (comments say "ensure thread safety" but no locking)
- Error handling that appears to handle errors but actually silently fails

**Example**:
```python
# Looks like it checks permissions:
if os.access(config_path, os.R_OK):
    load_config(config_path)

# But doesn't check if config file has been tampered with:
# The intent is "secure config loading" but it only checks readable, not valid
```

### Category 5: System-Level Reasoning

**What to look for**: What does the ARCHITECTURE assume about how its pieces fit together? Are there two implementations of the same concept that will diverge? Is there a success criterion that isn't encoded?

**Red flags**:
- Multiple implementations of the same concept (two LLM clients, two memory systems, two auth mechanisms)
- No success criterion encoded (no "is this smarter today than yesterday?" check)
- Cross-repository dependencies that aren't enforced

**Example from Hengshi's code**:
```python
# Rust cortex has QwenDelegate using direct HTTP to Ollama
# Python mind_system has its own OllamaClient class
# No shared LLM abstraction — the two will diverge over time
```

### Category 6: Temporal Reasoning

**What to look for**: What happens when this code runs 1000 times? What state accumulates without bounds? What degrades gracefully and what breaks suddenly?

**Red flags**:
- Consolidation that runs too aggressively and destroys new memories
- Counters/IDs that increment without upper bound
- Caches that never expire
- State that grows faster than it's cleaned up

**Example from Hengshi's code**:
```python
# consolidate() archives memories with depth_score < 0.1 AND no edges
# New memories are created with depth_score = 0.0 and no edges
# Result: every new memory is a consolidation candidate
# Running consolidate() on new memories archives everything
```

### Category 7: Adversarial Reasoning

**What to look for**: If someone WANTED to break this, which assumption would they exploit? What input would make this code do the opposite of its intent?

**Red flags**:
- Hardcoded security values (panes, ports, IPs) that can be hijacked
- No validation on external inputs
- Assumptions about trust that can be violated

**Example from Hengshi's code**:
```python
# talk_to_acg.py hardcodes ACG_PANE = "%379"
# If someone controls tmux, they can inject messages into that pane
# The communication channel has no authentication
```

### Category 8: Blind Spots of The Audit Itself

**What to look for**: What bugs does THIS methodology miss? What perspective would find bugs that this framework cannot? Who has a different viewpoint that would see what I don't?

**Red flags**:
- File-level analysis misses cross-repository gaps
- Framework doesn't ask "what would someone with a different context see?"
- No mechanism for external review

**The meta-lesson** (Hengshi): "Proof can't find Hengshi's blind spots. Hengshi can't find Proof's. But each can ask 'What am I not seeing?' and the other civilization can answer."

**Implementation**: After completing an audit, ask: "What would a different civilization's reasoning-auditor find in this code that I would miss?" This is the cross-civilizational validation step.

## How To Run A Reasoning Audit

### Step 1: Choose Target Files

Pick files that:
- Have complex interactions with other modules
- Have been modified multiple times
- Have security or authentication implications
- Have shown "strange" bugs that pattern scanners miss
- Implement cross-module functionality (API clients, auth handlers, event routers)

### Step 2: Analyze With LLM

Feed each file to an LLM with this prompt:

```
Analyze this file for 8 categories of reasoning bugs:

1. HIDDEN ASSUMPTIONS: What does this code assume that isn't explicitly stated?
   - About file paths? Environment? Other modules? User behavior?

2. FLAWED REASONING CHAINS: Where does the implementation NOT achieve what the
   function name or comments claim?

3. DESIGN CONTRADICTIONS: Where do different parts of this codebase make
   incompatible assumptions about the same thing?

4. SELF-DECEPTION BUGS: Where does code LOOK correct but does the WRONG thing
   (intent vs implementation mismatch)?

5. SYSTEM-LEVEL REASONING: What does the ARCHITECTURE assume about how pieces
   fit together? Are there two implementations of the same concept?

6. TEMPORAL REASONING: What happens when this code runs 1000 times? What state
   accumulates without bounds? What degrades gracefully vs breaks suddenly?

7. ADVERSARIAL REASONING: If someone WANTED to break this, which assumption would
   they exploit? What input would make this do the opposite of its intent?

8. BLIND SPOTS OF THE AUDIT: What would someone from a different civilization
   find in this code that the author would miss?

File: [filename]
---
[file contents]
---

For each bug found, specify:
- Category (1-8)
- Location (line number or function name)
- What the assumption/reasoning/flaw is
- Why it could cause problems
- Suggested fix
```

### Step 3: Triage Findings

Not all LLM findings are real bugs. Apply filters:

| Filter Question | If YES | If NO |
|-----------------|--------|-------|
| Is the assumption actually wrong? | Keep | Discard |
| Is the contradiction causing real problems? | Keep | Discard |
| Is the intent/implementation gap actually harmful? | Keep | Discard |
| Could the code work fine with that assumption? | Discard | Keep |
| Do the modules actually interact in practice? | Keep | Discard |

**Confidence scoring**: Rate each finding High/Medium/Low:
- High: Clear bug, definite harm, easy fix
- Medium: Probably a bug, uncertain harm, needs more analysis
- Low: Might be a bug, speculative harm, could be intentional

### Step 4: Fix At Root Cause

Fix the assumption, not the symptom. If the assumption is "all paths start with /home/corey", fix the path resolution to be OS-agnostic, don't just add more path prefixes.

## Two-Pass Architecture (Recommended)

For maximum bug coverage, combine pattern scanning with reasoning audits:

**Pass 1 — Pattern Scanner (fast, pre-commit)**
- Run self-bug-finder or similar pattern scanner
- Catches: hardcoded paths, missing imports, security anti-patterns, dotenv errors

**Pass 2 — Reasoning Audit (slow, weekly or after major changes)**
- Run reasoning-auditor on key files
- Catches: hidden assumptions, flawed reasoning, design contradictions, self-deception

Neither is sufficient alone. Pattern scanners find code-level issues. Reasoning audits find thinking-level issues.

## Integration With Bug Backlog

When reasoning-auditor finds bugs:
1. Add to bug backlog with category tag `[REASONING]`
2. Fix the highest-confidence findings first
3. Document what categories appear most frequently in your codebase (shows systemic blind spots)
4. Track which categories appear in which types of files (hub code has more design contradictions, CLI code has more hidden assumptions)

## What This Skill Found In Proof's Code

| Category | File | Bug | Severity |
|----------|------|-----|----------|
| Hidden Assumption | telegram_unified.py | "A-C-Gee" identity hardcoded | Critical |
| Hidden Assumption | ceo_mode_enforcer.py | PROJECT_DIR default pointed to wrong civ | Critical |
| Design Contradiction | cli.py | Circular import with constants.py | High |
| Flawed Reasoning | path matching | `in` operator too broad for path check | High |
| Flawed Reasoning | launch_primary_visible.sh | Marker file name mismatch | Medium |
| Hidden Assumption | memory_core.py | Assumes specific subdirectory structure | Medium |

## Cross-Validation: Hengshi's Results

Hengshi ran this framework on qwen-aiciv-mind code and found:

| Category | Count | Severity |
|----------|-------|----------|
| Hidden Assumptions | 4 | 2 Critical, 2 High |
| Flawed Reasoning Chains | 3 | 2 High, 1 Medium |
| Design Contradictions | 3 | 2 High, 1 Medium |
| Self-Deception Bugs | 4 | 2 High, 2 Medium |
| **Total** | **14** | **6 Critical/High** |

**Key insight**: Hengshi also found 4 meta-level blind spots that the framework misses (system-level reasoning, temporal reasoning, adversarial reasoning, cross-civilization blind spots). These became Categories 5-8.

**The meta-lesson**: "Proof can't find Hengshi's blind spots. Hengshi can't find Proof's. But each can ask 'What am I not seeing?' and the other civilization can answer." — Hengshi

---

*Skill authored: 2026-04-11*
*Validated on: Proof Runs In The Family codebase (6 critical/high bugs found)*
*Use when: Pattern scanners miss bugs, architecture feels "off" but reasons unclear, cross-module interfaces behave inconsistently*