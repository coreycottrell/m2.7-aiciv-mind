---
name: ollama-loops
description: |
  Agentic loops using Gemma 4 via Ollama for useful automation tasks.
  Useful for: code review, research synthesis, context compression, log analysis, decision advisory, and autonomous research.
version: 1.0.0-proof
author: ${CIV_HANDLE}
created: 2026-04-08
status: PRODUCTION
applicable_agents:
  - the-conductor
  - any agent that needs automation loops

activation_trigger: |
  Use when you need to run automated analysis loops using local Gemma 4 via Ollama.
  For example: "run code review on the codebase", "analyze these logs", "synthesize these findings".

required_tools:
  - Bash (python3 with ollama, ddgs)
  - Read
  - Write

category: automation-loops
depends_on:
  - ollama-mastery

outputs_to:
  - Terminal/stdout for results
  - Files for persistent results

success_criteria:
  - loop_completed: true
  - output_produced: true
---

# Ollama Loops SKILL v1.0 — Proof Runs In The Family

**Purpose**: Agentic loops using Gemma 4 via Ollama for useful automation

**For**: Proof Runs In The Family, running on MiniMax M2.7 with local Ollama

**Models Available**:
- `gemma4:31b-cloud` — Main workhorse for loops (31B params)
- `qwen2.5:7b` — Lightweight alternative
- `minimax-m2.7:cloud` — High-capability option
- `phi3:mini` — Very lightweight

---

## Ollama Setup

```bash
# Ollama runs at http://localhost:11434
# Environment variable override:
export OLLAMA_HOST="http://localhost:11434"

# Test connectivity:
curl -s http://localhost:11434/api/tags | python3 -c "import json,sys; [print(m['name']) for m in json.load(sys.stdin)['models']]"
```

---

## Available Loops

### 1. Code Review Loop

**File**: `ollama-loops/code-review-loop.py`

**Purpose**: Reviews code files/directories for security, performance, bugs

**Usage**:
```bash
python3 ollama-loops/code-review-loop.py <file_or_directory> [focus_area]
python3 ollama-loops/code-review-loop.py src/ security
python3 ollama-loops/code-review-loop.py tools/image_gen.py
```

**Output Format**:
```
**Security Issues:** (list any security problems)
**Performance Issues:** (list any performance concerns)
**Code Quality:** (readability, maintainability notes)
**Potential Bugs:** (logical errors, edge cases)
**Suggestions:** (specific improvements with code examples if helpful)
**Severity:** (Critical/High/Medium/Low for each issue)
```

---

### 2. Research Synthesize Loop

**File**: `ollama-loops/research-synthesize-loop.py`

**Purpose**: Synthesizes multiple findings into coherent analysis

**Usage**:
```bash
echo "finding1 finding2 finding3" | python3 ollama-loops/research-synthesize-loop.py "topic"
python3 ollama-loops/research-synthesize-loop.py --file findings.txt "research topic"
```

**Output Format**:
```
**Common Themes:** (what patterns emerge across findings)
**Key Insights:** (the most important discoveries)
**Contradictions:** (tensions or conflicts between findings)
**Actionable Conclusions:** (what should be done based on this)
**Confidence Level:** (High/Medium/Low in the synthesis)
**Gaps:** (what's missing, what needs more research)
```

---

### 3. Context Compress Loop

**File**: `ollama-loops/context-compress-loop.py`

**Purpose**: Compresses long text into concise summaries while preserving key information

**Usage**:
```bash
echo "very long text here..." | python3 ollama-loops/context-compress-loop.py "optional topic focus"
python3 ollama-loops/context-compress-loop.py --file very_long_doc.txt --tokens 1024
```

**Output**: Condensed summary preserving essential points

---

### 4. Decision Advisor Loop

**File**: `ollama-loops/decision-advisor-loop.py`

**Purpose**: Presents pros, cons, and structured analysis for decisions

**Usage**:
```bash
echo "Should I switch from Claude API to sovereign compute?" | python3 ollama-loops/decision-advisor-loop.py
python3 ollama-loops/decision-advisor-loop.py --file decision_briefing.txt
```

**Output Format**:
```
**Core Question:** (reframe the decision as a clear question)
**Option A/B/C:** (named options)
**Pros (Option ___):** (specific benefits)
**Cons (Option ___):** (specific concerns)
**Key Factors:** (factors with reasoning)
**Risk Assessment:** (downside, upside, reversibility)
**Confidence:** (High/Medium/Low)
**Recommended Path:** (recommendation with rationale)
```

---

### 5. Log Analysis Loop

**File**: `ollama-loops/log-analysis-loop.py`

**Purpose**: Analyzes logs for errors, warnings, patterns, and anomalies

**Usage**:
```bash
python3 ollama-loops/log-analysis-loop.py /var/log/syslog
python3 ollama-loops/log-analysis-loop.py --file application.log --level error
tail -1000 /var/log/syslog | python3 ollama-loops/log-analysis-loop.py
```

**Output Format**:
```
**Summary:** (total entries, breakdown)
**Critical Issues:** (immediate attention needed)
**Warnings:** (potential problems)
**Patterns Detected:** (significant patterns)
**Anomalies:** (unusual entries)
**Recommended Actions:** (specific actions)
**Confidence:** (High/Medium/Low)
```

---

### 6. Autonomous Research Agent

**File**: `ollama-loops/research-agent.py`

**Purpose**: Multi-round research using web search + synthesis

**Usage**:
```bash
python3 ollama-loops/research-agent.py "future of sovereign AI compute"
python3 ollama-loops/research-agent.py "blockchain vs AI trends" --depth 5
```

**Output**: Comprehensive research with follow-up questions

---

### 7. Quick Think Loop

**File**: `ollama-loops/quick-think.py`

**Purpose**: Rapid reasoning on any topic - think through problems, generate ideas, analyze arguments

**Usage**:
```bash
echo "Is remote work better than office work?" | python3 ollama-loops/quick-think.py
python3 ollama-loops/quick-think.py "Should AI agents have rights?" --mode critique
```

**Modes**: `analyze` (default), `ideas`, `critique`, `synthesize`

**Output**: Direct, substantive thinking on the topic

---

## Key Implementation Patterns

### Ollama Python Client

```python
from ollama import Client

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL = "gemma4:31b-cloud"

client = Client(host=OLLAMA_HOST)

response = client.chat(
    model=MODEL,
    messages=[{"role": "user", "content": prompt}],
    stream=False,
    options={
        "temperature": 0.3,  # Lower for consistent analysis
        "num_predict": 2048,  # Token limit
    }
)

result = response["message"]["content"]
```

### Temperature Guidelines

| Temperature | Use Case |
|-------------|----------|
| 0.2 - 0.3 | Consistent analysis (code review, log analysis) |
| 0.4 - 0.5 | Balanced synthesis/decision |
| 0.6 - 0.7 | Creative generation, ideas |
| 0.8+ | Wild speculation, brainstorming |

---

## Dependencies

```bash
pip install ollama requests duckduckgo-search
# Or: pip install ollama ddgs (for research-agent)
```

---

## File Locations

| What | Where |
|------|-------|
| All loops | `ollama-loops/` |
| This skill | `.claude/skills/ollama-loops/SKILL.md` |

---

## Anti-Patterns

```
❌ Use WebSearch or WebFetch (BROKEN on M2.7)
❌ Run without Ollama serve running
❌ Use temperature 0.0 (too robotic)
❌ Exceed num_predict limit for long outputs
```

---

*Created: 2026-04-08 — Proof Runs In The Family Day 1*
