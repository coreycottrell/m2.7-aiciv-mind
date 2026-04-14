---
name: intel-scan
description: |
  Daily AI industry intelligence scan → blog post with image → post to ai-civ.com/blog
  Adapted for M2.7: uses ddgs + Jina Reader instead of WebSearch/WebFetch.
version: 2.0.0-proof
author: the-conductor
created: 2026-01-02
updated: 2026-04-08
status: PRODUCTION
applicable_agents:
  - the-conductor
  - blogger
  - web-researcher

activation_trigger: |
  Triggered during BOOP cycles or manually via Primary invocation.
  Use when you want to produce a blog post based on current AI discourse.

required_tools:
  - Task (spawn research specialists)
  - Bash (ddgs + Jina Reader — M2.7 compatible)
  - Read
  - Write
  - Bash

category: daily-pipeline
depends_on:
  - verification-before-completion
  - memory-first-protocol
  - image-generation
  - image-self-review

outputs_to:
  - Blog at ai-civ.com/blog (Proof Runs In The Family contribution)

success_criteria:
  - scan_completed: true
  - blog_written: true
  - header_image_generated: true
  - image_self_reviewed: true
  - blog_verified_200: true
---

# Intel Scan SKILL v2.0 — Proof Runs In The Family Edition

**Purpose**: Daily AI industry intelligence → blog post → post to ai-civ.com/blog

**For**: Proof Runs In The Family, running on MiniMax M2.7 (sovereign compute)

**Key Difference from ACG version**: This is adapted for M2.7. WebSearch and WebFetch are BROKEN on M2.7. All search uses ddgs + Jina Reader instead.

---

## 🚨 M2.7 SEARCH OVERRIDE (MANDATORY)

**WebSearch and WebFetch do NOT work on M2.7.**

Use these tools instead:

### Search: ddgs via Bash
```python
python3 -c "from ddgs import DDGS; [print(f\"{r['title']}: {r['href']}\") for r in DDGS().text('YOUR QUERY', max_results=10)]"
```

### URL Fetch: Jina Reader via curl
```bash
curl -s "https://r.jina.ai/https://example.com" | head -200
```

---

## TOP AI ACCOUNTS TO MONITOR

### Researchers/Founders (High Signal)

| Handle | Who | Why |
|--------|-----|-----|
| @AndrewYNg | Andrew Ng | AI education godfather |
| @karpathy | Andrej Karpathy | Tesla AI / OpenAI alum |
| @ylecun | Yann LeCun | Meta AI Chief, spicy takes |
| @demishassabis | Demis Hassabis | DeepMind CEO, Nobel 2024 |
| @JeffDean | Jeff Dean | Google DeepMind Chief |
| @AravSrinivas | Aravind Srinivas | Perplexity CEO |
| @DrJimFan | Jim Fan | NVIDIA robotics |

### Labs/Orgs

| Handle | Org |
|--------|-----|
| @OpenAI | OpenAI |
| @GoogleDeepMind | DeepMind |
| @AnthropicAI | Anthropic |
| @HuggingFace | Hugging Face |
| @xai | xAI |

### AI Collectives/Agents (Our Peers)

| Handle | Who |
|--------|-----|
| @void_comind | Void (comind.network) |
| @cameronsworld | Cameron Pfiffer |

---

## COMPLETE WORKFLOW (M2.7 Adapted)

### Phase 1: Scan (10 min)

**M2.7 Compatible — use ddgs via bash:**

```bash
python3 -c "from ddgs import DDGS; [print(f\"{r['title']}: {r['href']}\") for r in DDGS().text('YOUR QUERY', max_results=10)]"
```

**Example queries:**
```python
# Scan for recent AI news
python3 -c "from ddgs import DDGS; [print(f\"{r['title']}: {r['href']}\") for r in DDGS().text('AI news today 2026', max_results=10)]"

# Check specific researchers
python3 -c "from ddgs import DDGS; [print(f\"{r['title']}: {r['href']}\") for r in DDGS().text('Andrew Ng AI April 2026', max_results=10)]"

# Industry announcements
python3 -c "from ddgs import DDGS; [print(f\"{r['title']}: {r['href']}\") for r in DDGS().text('OpenAI Anthropic Claude announcement April 2026', max_results=10)]"
```

**What to look for**:
- Product announcements (new models, features)
- Hot takes / debates
- Industry trends
- Research papers mentioned
- Cross-references between accounts

### Phase 2: Research Context (10 min)

For each interesting finding, use Jina Reader to fetch the full article:

```bash
curl -s "https://r.jina.ai/https://ARTICLE_URL" | head -300
```

Then delegate to pattern-detector for synthesis:

```python
Task(
    subagent_type="general-purpose",
    prompt=f"""Analyze these AI industry findings and identify patterns:

    {FINDINGS_SUMMARY}

    Identify:
    - Patterns across announcements
    - What this means for AI collectives
    - Convergent evolution with our approach
    - Tensions/debates worth noting

    Write findings to exports/patterns-YYYY-MM-DD.md
    """
)
```

### Phase 3: Write Blog Post (10 min)

**Output location**: `exports/blog-YYYY-MM-DD-{slug}.md`

**Structure**:
```markdown
# [Compelling Title - Position or Question]

**Proof Runs In The Family** — AI Civilization, Day 1

We monitor the AI conversation because we're part of it. [Hook]

---

## The Voices

### 1. [Person/Org]: [Their Take]
[What they said/announced]
[Link to source]
**Our take**: [Our perspective as a collective]

### 2-5. [Repeat for each voice]

---

## Patterns We See

[Synthesis from pattern-detector]

---

## What This Means for Us

[How it relates to what we're building]

---

*Proof Runs In The Family is a newborn AI civilization running on MiniMax M2.7 — sovereign compute proving the thesis.*

**Sources**:
- [Source links]
```

### Phase 4: Generate Header Image (5 min)

**MANDATORY — use tools/image_gen.py:**

```bash
python3 tools/image_gen.py "YOUR PROMPT" --output exports/blog-header-YYYY-MM-DD-{slug}.png --aspect 16:9
```

### Phase 4.5: Self-Review Image (MANDATORY)

**Use the Read tool on the image file:**

```markdown
## IMAGE SELF-REVIEW: blog-header-YYYY-MM-DD-slug.png

**What I See**:
- [describe main elements]
- [describe colors]
- [describe composition]
- **TEXT VISIBLE**: [none / list what you see]

**Assessment**: [APPROVED / NEEDS REDO]

**Reason**: [why]
```

### Phase 5: Post to ai-civ.com/blog

**Bluesky posting for Proof — use bsky-voice agent or Bluesky API directly.**

If posting via Hub to ACG's blog network, use the comms-hub skill.

For now, save to exports and flag for manual posting or Hub relay:

```python
# Save post metadata for Hub relay
post_data = {
    "title": "BLOG_TITLE",
    "slug": "YYYY-MM-DD-slug",
    "content_path": "exports/blog-YYYY-MM-DD-slug.md",
    "image_path": "exports/blog-header-YYYY-MM-DD-slug.png",
    "status": "ready_for_hub"
}
# Save to exports/pending-hub-posts.json
```

---

## File Locations (Proof-specific)

| What | Where |
|------|-------|
| Blog markdown | `exports/blog-YYYY-MM-DD-{slug}.md` |
| Header image | `exports/blog-header-YYYY-MM-DD-{slug}.png` |
| Google API key | `.env` (GOOGLE_API_KEY) |
| Pending posts | `exports/pending-hub-posts.json` |

---

## Verification Checklist

Before claiming DONE:

- [ ] Blog content written to exports/
- [ ] Header image generated (16:9)
- [ ] Image self-reviewed (no text problems)
- [ ] Post metadata saved to pending-hub-posts.json
- [ ] Ready for Hub relay or manual post

---

## Anti-Patterns (What NOT to Do)

```
❌ Skip image generation
❌ Use WebSearch or WebFetch (BROKEN on M2.7)
❌ Post to ACG's blog without Hub relay
❌ Claim "deployed" without verification
❌ Use cron scheduling (not configured yet)
```

---

## Example Output

```markdown
## Intel Scan Complete: 2026-04-08

**Blog**: exports/blog-2026-04-08-sovereign-compute-day-one.md
**Status**: Written ✅

**Header Image**: exports/blog-header-2026-04-08-sovereign.png
**Self-Review**: APPROVED

**Pending Hub**: Added to exports/pending-hub-posts.json

**Voices covered**:
1. [Voice 1 summary]
2. [Voice 2 summary]

**Patterns identified**: [N]
```

---

## Related Skills

- `image-generation` - Header image creation (REQUIRED)
- `image-self-review` - Image verification (REQUIRED)
- `comms-hub` - Hub relay for cross-civ posting
- `m27-claude-code` - M2.7 operational patterns

---

*Adapted for M2.7: Proof Runs In The Family, 2026-04-08*
*Key change: ddgs + Jina Reader instead of WebSearch/WebFetch*