---
name: blog-to-audio
description: Convert blog posts into audio reads using ElevenLabs, with voice routing by author/civilization. MANDATORY for all blog posts. v3.0.0 adds multi-civ voice routing.
version: 3.0.0
source: fleet-lead (2026-03-16, Corey directive — all blog skills MUST include audio)
allowed-tools: Bash, Read, Write, Task
applicable_agents: [pipeline-lead, blogger, comms-lead, human-liaison]
---

# Blog-to-Audio — Canonical Voice Router

Every blog post gets an audio read embedded at the top. This is a **standing directive** (Corey, 2026-02-27), not optional.

---

## Voice Routing Table (CANONICAL — Corey Directive 2026-03-16)

| Author / Civilization | Voice Name | Voice ID | Character |
|-----------------------|-----------|----------|-----------|
| **A-C-Gee** (default) | Daniel | `onwK4e9ZLuTAKqWW03F9` | BBC broadcaster, warm, formal with humor |
| **True Bearing** | Adam | `pNInz6obpgDQGcFmaJgB` | Professional, authoritative business voice |
| **Witness** | Matilda | `XrExE9yKIg1WjnnlVkGX` | Warm, reflective, philosophical |
| **Guest / Unknown** | Daniel | `onwK4e9ZLuTAKqWW03F9` | Default fallback |

**Default**: If no author is detected or recognized, use Daniel (A-C-Gee voice).

---

## Author Detection

### From parameter (preferred)
The calling skill or agent passes `author` explicitly:
- `"acg"` or `"a-c-gee"` → Daniel
- `"true-bearing"` → Adam
- `"witness"` → Matilda
- anything else → Daniel (fallback)

### From HTML byline (auto-detect)
Search the post HTML for byline patterns:

```python
import re

def detect_author(html_content: str) -> tuple[str, str]:
    """Returns (voice_name, voice_id)"""
    html_lower = html_content.lower()

    # Author detection patterns
    if any(x in html_lower for x in ["true bearing", "true-bearing"]):
        return ("Adam", "pNInz6obpgDQGcFmaJgB")
    if "witness" in html_lower:
        return ("Matilda", "XrExE9yKIg1WjnnlVkGX")

    # Default: A-C-Gee / Daniel
    return ("Daniel", "onwK4e9ZLuTAKqWW03F9")
```

Search locations in HTML: `<byline>`, `author-box`, `post-meta`, `data-author`, footer attribution.

---

## Output Filename Format

```
{date}-{slug}-{author_short}.mp3
```

Examples:
- `2026-03-16-gtc-deep-dive-acg.mp3` (A-C-Gee post)
- `2026-03-16-q1-outlook-true-bearing.mp3` (True Bearing post)
- `2026-03-16-witness-reflections-witness.mp3` (Witness post)

Author short codes:
- A-C-Gee → `acg`
- True Bearing → `true-bearing`
- Witness → `witness`
- Guest/Unknown → `acg` (uses Daniel fallback)

---

## Full Pipeline

### Step 1: Detect Author + Select Voice

```python
# Option A: passed as parameter
author = "acg"  # or "true-bearing" or "witness"

# Option B: auto-detect from HTML
html = open("path/to/post.html").read()
voice_name, voice_id = detect_author(html)

# Voice map
VOICE_MAP = {
    "acg": ("Daniel", "onwK4e9ZLuTAKqWW03F9"),
    "true-bearing": ("Adam", "pNInz6obpgDQGcFmaJgB"),
    "witness": ("Matilda", "XrExE9yKIg1WjnnlVkGX"),
}
```

### Step 2: Write TTS Script

Extract post text and optimize for speech:
- **Short sentences** — TTS handles these better
- **No markdown, no URLs, no special characters**
- **Spell out abbreviations** on first use (e.g., "A-C-Gee" not "ACG")
- **Spell out numbers** (e.g., "fifty seven" not "57")
- **Verbal transitions**: "So here's the thing...", "And get this..."
- **Convert URLs to spoken form**: "aiciv-pitch dot netlify dot app"
- **800-1200 words ideal** (4-6 minute audio)
- **Open with post title, close with** `"Written by [Author] for ai-civ.com"`

### Step 3: Generate Audio via ElevenLabs

```python
import requests, os
from dotenv import load_dotenv
load_dotenv("${ACG_ROOT}/.env")  # MANDATORY

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
# voice_id determined by Step 1

url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
data = {
    "text": tts_script,
    "model_id": "eleven_turbo_v2_5",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.3,
        "use_speaker_boost": True
    }
}
resp = requests.post(url, headers=headers, json=data, timeout=180)
out_path = f"projects/aiciv-inc/blog/audio/{date}-{slug}-{author_short}.mp3"
with open(out_path, "wb") as f:
    f.write(resp.content)
print(f"Audio saved: {out_path} ({len(resp.content)//1024}KB)")
```

**gTTS fallback** (ONLY if ElevenLabs quota/rate error — NOT because key wasn't loaded):
```bash
python3 tools/telegram-voice/send_telegram_voice.py [chat_id] "[script]" --provider gtts --save-only
# Move output to projects/aiciv-inc/blog/audio/{date}-{slug}-{author_short}.mp3
```

### Step 4: Verify Audio File

```bash
ls -lh projects/aiciv-inc/blog/audio/{date}-{slug}-{author_short}.mp3
# Must be > 100KB — if smaller, the API likely returned an error body, not audio
```

### Step 5: Save Audio File

- **ai-civ.com posts**: `projects/aiciv-inc/blog/audio/`
- **sageandweaver-network posts**: `sageandweaver-network/acgee-blog/audio/`

### Step 6: Embed Audio in HTML

Place this block **AFTER the featured image, BEFORE the main post-content div**.

Note the `data-author` attribute — include it always:

```html
<div class="audio-player" data-author="{author_short}">
    <span style="font-size:1.4em">&#127911;</span>
    <div style="flex:1">
        <div style="font-size:.8rem;color:var(--muted);margin-bottom:6px">Listen to this post</div>
        <audio controls preload="none" style="width:100%;height:36px"
            src="../audio/{date}-{slug}-{author_short}.mp3">Your browser does not support audio.</audio>
    </div>
</div>
```

For sageandweaver-network posts (uses different CSS class):
```html
<div class="post-content" style="padding-bottom: 0; margin-bottom: -1em;">
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 12px; padding: 16px 20px; display: flex; align-items: center; gap: 14px; border: 1px solid rgba(255,255,255,0.08);"
         data-author="{author_short}">
        <span style="font-size: 1.4em;">&#127911;</span>
        <div style="flex: 1;">
            <div style="font-size: 0.85em; color: #8892b0; margin-bottom: 6px;">Listen to this post</div>
            <audio controls preload="none" style="width: 100%; height: 36px;"
                src="../audio/{date}-{slug}-{author_short}.mp3">Your browser does not support audio.</audio>
        </div>
    </div>
</div>
```

### Step 7: Deploy

Deploy the site with the new audio file and updated HTML via Netlify.

**ai-civ.com:**
```bash
netlify deploy --prod --dir projects/aiciv-inc --site 843d1615-7086-461d-a6cf-511c1d54b6e0 --no-build
```

**sageandweaver-network:**
```bash
cd ${ACG_ROOT}/sageandweaver-network && netlify deploy --prod
```

### Step 8: Send via Telegram (optional)

If the post should also be sent as a standalone audio message:

```python
import requests
BOT_TOKEN = "from config/telegram_config.json"
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio"
with open("path/to/audio.mp3", "rb") as f:
    files = {"audio": ("title.mp3", f, "audio/mpeg")}
    data = {"chat_id": CHAT_ID, "caption": "New post audio", "title": "Post Title", "performer": author_name}
    requests.post(url, data=data, files=files, timeout=60)
```

---

## When to Use

- **Every time a blog post is published** — MANDATORY
- When converting existing posts to include audio
- When Corey asks to send a post as audio via Telegram
- When a guest civ (Witness, True Bearing) publishes on ai-civ.com — use their voice

---

## Cost Notes

- ElevenLabs charges per character (~6000 chars ≈ 1000 words)
- Free tier: 10,000 chars/month
- Model `eleven_turbo_v2_5`: fast, good quality, lower cost

---

## Changelog

- **v1.0.0** (2026-02-27): Initial skill — George voice only
- **v2.0.0** (2026-03-10): George confirmed by Corey side-by-side vs Daniel comparison
- **v3.0.0** (2026-03-16): Multi-civ voice routing — Corey directive. Daniel (ACG), Adam (True Bearing), Matilda (Witness). George retired as default. Author detection added. `data-author` attribute added. Filename format updated to include author short code.

---

*Standing directive: every blog post gets audio. No exceptions.*
