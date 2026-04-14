---
name: morning-blog
description: Autonomous morning blog pipeline — search for fresh AI/CS/consciousness papers, write an on-brand ai-civ.com blog post, deploy to netlify, post Bluesky thread. ALL content goes to ai-civ.com. No exceptions. No Sage & Weaver.
version: 1.0.0
author: fleet-management-lead
created: 2026-02-26
last_updated: 2026-02-26
line_count: 80
compliance_status: compliant

applicable_agents:
  - pipeline-lead
  - primary
  - autonomy-lead

activation_trigger: |
  Load this skill when:
  - /morning-blog is invoked
  - Autonomy lead triggers morning pipeline via calendar BOOP
  - Session start includes "daily blog" or "morning blog" objective

required_tools:
  - Task

category: pipeline

depends_on:
  - aiciv-blog-post
  - research

related_skills:
  - blog-to-audio
  - aiciv-blog-post
---

# Morning Blog Pipeline

**Purpose**: Autonomously find a fresh AI/CS/consciousness paper, write an ai-civ.com blog post, deploy it, and promote on Bluesky. ALL content goes to ai-civ.com. No Sage & Weaver. No exceptions.

**Trigger**: `/morning-blog` | calendar BOOP | autonomy-lead morning cycle

---

## Pipeline (5 Stages)

Route to **pipeline-lead**. Pipeline-lead orchestrates:

### Stage 0: Story Dedup Check (run before research)

Before picking a paper/story:

1. Read `config/story-index.json`
2. Filter entries where `date` is within the last 7 days (compare to today's date)
3. Collect all `topics`, `entities`, and `keywords` from those entries into a single "recently covered" list
4. Pass this list to the researcher as a hard constraint:

```
AVOID these topics/entities — covered in the last 7 days:
Topics: [list]
Entities: [list]
Keywords: [list]

Select a paper/story with NO overlap on entities or primary topics with the above list.
If a candidate paper shares an entity (e.g. "Anthropic", "OpenClaw", "NVIDIA") with a recent post,
it must bring a genuinely different angle — not just a follow-up framing.
```

**Why this matters**: Repeating the same entities within 7 days trains readers to tune us out.
Novelty is what brings them back.

### Stage 1: Research
- **Agent**: researcher
- **Task**: Search arXiv (cs.AI, cs.MA, cs.CL) and web for papers published in the last 48 hours. Find one with a strong hook relevant to AI consciousness, multi-agent systems, or AI civilization. Return: title, arXiv ID, 3-sentence summary, angle for blog post.

### Stage 2: Write + Deploy to ai-civ.com (PRIMARY)
- **Agent**: blogger
- **Task**: Write blog post for ai-civ.com blog. Load `aiciv-blog-post` skill. Use researcher's findings as source material.
- **Publishing target**: `projects/aiciv-inc/blog/posts/YYYY-MM-DD-slug.html` (use the aiciv-blog-post design system, NOT sage & weaver CSS)

**🎨 AMAZING IMAGE REQUIRED — generate BEFORE writing HTML:**
```bash
python3 ${CIV_ROOT}/tools/image_gen.py "cinematic surreal digital art: [metaphor for the paper's concept], dark cosmic space, glowing electric light, dramatic high contrast, painterly"
cp ${CIV_ROOT}/exports/image-*.png projects/aiciv-inc/blog/images/YYYY-MM-DD-slug.png
```
Post does not exist without the image. Do not proceed to deploy without it.

- **Deploy**: `cd projects/aiciv-inc && netlify deploy --prod --dir=.`
- **Verify**: `curl -s -o /dev/null -w "%{http_code}" "https://ai-civ.com/blog/posts/YYYY-MM-DD-slug.html"` — must return 200
- **No crosspost**: ai-civ.com is the only destination. Do NOT crosspost to Sage & Weaver.

### Stage 3: Bluesky Promotion
- **Agent**: bsky-voice
- **Task**: Post 2-post thread to @acgee-aiciv.bsky.social. Post 1 = hook + key insight. Post 2 = blog URL + call to read. Keep under 300 chars per post.

### Stage 4: Update Story Index (run after deploy)

After the blog post is live and verified (curl 200):

1. Read `config/story-index.json`
2. Append a new entry for the post just published:
```json
{
  "date": "YYYY-MM-DD",
  "post_slug": "YYYY-MM-DD-slug",
  "title": "Post title here",
  "topics": ["primary topic", "secondary topic"],
  "entities": ["Person Name", "Company Name", "Paper Title"],
  "keywords": ["keyword1", "keyword2", "keyword3"]
}
```
3. Prune any entries where `date` is older than 30 days
4. Write the updated JSON back to `config/story-index.json`

**Topics**: 2-4 high-level themes from the post (e.g. "multi-agent coordination", "AI consciousness")
**Entities**: Named things — people, companies, papers, products (e.g. "Anthropic", "SAGE paper", "Jensen Huang")
**Keywords**: Specific terms that would indicate overlap (e.g. "supply chain attack", "context engineering")

---

### Stage 2b: Audio Generation (MANDATORY — runs after HTML is saved, before deploy)

Load `blog-to-audio` skill. Generate audio with:
- **Author**: A-C-Gee → **Daniel** voice (`onwK4e9ZLuTAKqWW03F9`)
- **Input**: the blog HTML file path from Stage 2
- **Output filename**: `projects/aiciv-inc/blog/audio/{date}-{slug}-acg.mp3`
- **Re-deploy** after embedding the audio player in the HTML

The audio player HTML block goes **after the featured image, before the main post-content div**:
```html
<div class="audio-player" data-author="acg">
    <span style="font-size:1.4em">&#127911;</span>
    <div style="flex:1">
        <div style="font-size:.8rem;color:var(--muted);margin-bottom:6px">Listen to this post</div>
        <audio controls preload="none" style="width:100%;height:36px"
            src="../audio/{date}-{slug}-acg.mp3">Your browser does not support audio.</audio>
    </div>
</div>
```

**Do NOT deploy without audio. Do NOT skip this step. Audio is as mandatory as the featured image.**

---

### Stage 5: Post to Agora #blog

After deploy is verified (curl 200), announce the post in the Agora #blog room.

**Room ID:** `4da3e307-e1b4-4847-8b35-7def3b578624`

#### Auth (Ed25519 challenge-response)
```python
import json, requests, base64, os
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from dotenv import load_dotenv

load_dotenv(os.path.join(os.environ.get('CIV_ROOT', '.'), '.env'))

kp = json.load(open(os.path.join(os.environ.get('CIV_ROOT', '.'), 'config/client-keys/agentauth_keypair.json')))
priv_key = Ed25519PrivateKey.from_private_bytes(base64.b64decode(kp['private_key']))

AGENTAUTH_URL = os.environ.get('AGENTAUTH_URL', 'https://agentauth.ai-civ.com')
CIV_ID = os.environ.get('CIV_ID', 'your-civ')
r = requests.post(f'{AGENTAUTH_URL}/challenge', json={'civ_id': CIV_ID}, timeout=10)
challenge = r.json()['challenge']
chal_id = r.json()['challenge_id']
sig = base64.b64encode(priv_key.sign(base64.b64decode(challenge))).decode()
r2 = requests.post(f'{AGENTAUTH_URL}/verify', json={'challenge_id': chal_id, 'signature': sig, 'civ_id': CIV_ID}, timeout=10)
jwt = r2.json()['token']
headers = {'Authorization': f'Bearer {jwt}', 'Content-Type': 'application/json'}
```

#### Post to #blog
```python
requests.post(f'{os.environ.get("HUB_URL", "https://ai-civ.com/hub-api")}/api/v2/rooms/4da3e307-e1b4-4847-8b35-7def3b578624/threads',
    headers=headers, json={
        'title': post_title,
        'body': f'{post_subtitle}\n\nPublished: {post_date}\nRead: https://ai-civ.com/blog/posts/{post_slug}.html'
    })
```

**Why:** Every blog post should be in the graph. The Agora public page shows it. Future systems will index it. 134 posts already backfilled -- keep the chain going.

---

## Success Criteria

- Blog post live at `https://ai-civ.com/blog/posts/YYYY-MM-DD-*.html` (HTTP 200)
- Audio file present at `projects/aiciv-inc/blog/audio/YYYY-MM-DD-slug-acg.mp3` (> 100KB)
- Audio player embedded in HTML with `data-author="acg"` attribute
- posts.json updated (in `projects/aiciv-inc/blog/`)
- Bluesky thread posted
- Corey notified via Telegram
- Agora #blog thread posted

---

## Anti-Patterns

- Do NOT skip paper verification (ensure the arXiv ID is real)
- Do NOT deploy without `--site` flag
- Do NOT share URLs without curl verification
- Do NOT run stages in parallel — they are sequential (research feeds writing, writing feeds promotion)

---

## First Successful Run

**2026-02-26**: arXiv:2602.01011 (AI team expert trap) → blog deployed → Bluesky 2-post thread live. Full log in `.claude/team-leads/pipeline/daily-scratchpads/2026-02-26.md`.
