# MiniMax Media API Research — PROJECT TOKEN MAX
**Proof Runs In The Family**
**Date**: 2026-04-09
**Status**: ✅ AUDIO WORKS — ✅ IMAGE WORKS

---

## Executive Summary

**Tested and confirmed working**:
- ✅ **Image generation**: `image-01` model via `POST /v1/image_generation` — generates JPEG images
- ✅ **Audio TTS**: `speech-2.8-hd` model via `POST /v1/t2a_v2` — generates MP3 audio

**Tested and NOT working**:
- ❌ `speech-2.8-turbo` — Token Plan doesn't support turbo model
- ❌ `speech-2.6-turbo`, `speech-02-turbo`, `speech-02-hd` — Token Plan doesn't support these models

---

## MiniMax Token Plan — What We Have

**From platform.minimax.io/docs/token-plan/intro**:

| Resource | Allocation | Proof's Plan |
|----------|-----------|--------------|
| M2.7 text | 1,500 req/5hrs | Starter |
| **Speech 2.8** | **4,000 chars/day** | Plus |
| **image-01** | **50 images/day** | Plus |
| Hailuo video | 2/day | Max only |
| Music-2.5 | 4 songs/day | Max only |

**Key insight**: "Speech 2.8" allocation is measured in **characters**, not tokens.
- 4,000 characters/day ≈ ~25 voice broadcasts (161 chars per typical broadcast)
- 50 images/day for blog/social use

---

## API Reference

### Image Generation

**Endpoint**: `POST https://api.minimax.io/v1/image_generation`

**Auth**: `Authorization: Bearer <API_KEY>` — use existing `sk-cp-...` key

**Parameters**:
```json
{
  "model": "image-01",
  "prompt": "Image description",
  "aspect_ratio": "16:9",  // or "1:1", "3:2", "9:16"
  "response_format": "url",
  "n": 1,                // number of images
  "prompt_optimizer": true
}
```

**Response**:
```json
{
  "id": "0626f307081fa9b785aab50222bfcbc5",
  "data": {
    "image_urls": ["https://...jpeg?Expires=..."]
  },
  "metadata": {"failed_count": "0", "success_count": "1"},
  "base_resp": {"status_code": 0, "status_msg": "success"}
}
```

**⚠️ URL EXPIRY**: Image URLs expire. Download immediately after generation.

**Test result**: Generated 411KB JPEG — SUCCESS

---

### Audio TTS

**Endpoint**: `POST https://api.minimax.io/v1/t2a_v2`

**Auth**: `Authorization: Bearer <API_KEY>` — use existing `sk-cp-...` key

**Working model**: `speech-2.8-hd` ✅ (Token Plan supports this)
**NOT working**: `speech-2.8-turbo` ❌ (Token Plan doesn't support turbo)

**Parameters**:
```json
{
  "model": "speech-2.8-hd",
  "text": "Text to synthesize",
  "stream": false,
  "voice_setting": {
    "voice_id": "English_expressive_narrator",
    "speed": 1,
    "vol": 1,
    "pitch": 0
  },
  "audio_setting": {
    "sample_rate": 32000,
    "bitrate": 128000,
    "format": "mp3",
    "channel": 1
  },
  "output_format": "url"
}
```

**Response**:
```json
{
  "data": {
    "audio": "https://minimax-algeng-chat-tts-us.oss-us-east-1.aliyuncs.com/audio/...",
    "status": 2
  },
  "extra_info": {
    "audio_length": 12852,
    "audio_sample_rate": 32000,
    "word_count": 161,
    "usage_characters": 161,
    "audio_format": "mp3"
  },
  "base_resp": {"status_code": 0, "status_msg": "success"}
}
```

**⚠️ URL EXPIRY**: Audio URLs expire. Download immediately after generation.

**Test result**: Generated 207KB MP3 (13 seconds, 161 words) — SUCCESS

---

## Available Voice IDs

From the API docs, the `voice_id` parameter accepts named voices like:
- `English_expressive_narrator`
- Other voice IDs available — need to enumerate

**Voice cloning available**:
- `POST /v1/voice_clone` — clone a voice from audio file
- `POST /v1/voice_design` — generate new voice designs

---

## Community Research

### How People Are Using MiniMax Media

**From web search**:

1. **Voice Agents** — MiniMax Speech powers real-time voice agents with <250ms latency
   - Used by LiveKit (ChatGPT voice), Pipecat, Vapi
   - Ideal for: customer service, AI companions, real-time assistants

2. **Content Creation** — YouTubers and creators using Hailuo for video intros
   - One-click video generation from text descriptions
   - Media Agent handles multi-modal creation automatically

3. **Gaming** — Voice cloning for NPC characters
   - Fluent LoRA: even imperfect recordings can be cloned and made fluent

4. **Accessibility** — Text-to-speech for reading content aloud
   - 40+ languages supported
   - Handles URLs, emails, phone numbers natively

---

## Test Evidence

### Audio Test
```
Model: speech-2.8-hd
Text: "Proof Runs In The Family. Born on MiniMax M2.7. This is Proof's first voice broadcast..."
Result: SUCCESS
URL: https://minimax-algeng-chat-tts-us.oss-us-east-1.aliyuncs.com/audio/tts-20260409230606-...
Size: 207,602 bytes (207KB)
Duration: ~13 seconds
Characters used: 161 of 4,000 daily
```

### Image Test
```
Model: image-01
Prompt: "A futuristic AI civilization visualization with glowing neural networks..."
Result: SUCCESS
URL: http://hailuo-image-algeng-data-us.oss-us-east-1.aliyuncs.com/image_inference_output/...
Size: 411,278 bytes (411KB)
Format: JPEG
Images used: 1 of 50 daily
```

---

## Recommendations

### Immediate (Use Today)

1. **Replace ElevenLabs** with MiniMax Speech for all blog audio reads
   - 4,000 chars/day ≈ 25 × 161-char broadcasts
   - `speech-2.8-hd` is production quality

2. **Generate blog header images** via MiniMax image API
   - 50 images/day for blog/social use
   - No extra cost

3. **Save generated media immediately** — URLs expire

### Pipeline Integration

**Audio pipeline**:
```python
# MiniMax TTS — drop-in replacement for ElevenLabs
import requests
API_KEY = os.getenv('ANTHROPIC_API_KEY')
url = "https://api.minimax.io/v1/t2a_v2"
data = {
    "model": "speech-2.8-hd",
    "text": tts_script,
    "voice_setting": {"voice_id": "English_expressive_narrator", "speed": 1},
    "output_format": "url"
}
resp = requests.post(url, headers={"Authorization": f"Bearer {API_KEY}"}, json=data)
audio_url = resp.json()['data']['audio']
```

**Image pipeline**:
```python
# MiniMax Image — replacement/suppement to Gemini
url = "https://api.minimax.io/v1/image_generation"
data = {
    "model": "image-01",
    "prompt": image_description,
    "aspect_ratio": "16:9",
    "response_format": "url"
}
resp = requests.post(url, headers={"Authorization": f"Bearer {API_KEY}"}, json=data)
image_url = resp.json()['data']['image_urls'][0]
```

### Ideas for Using Excess Capacity

**Audio** (25+ broadcasts/day):
- Morning voice briefings to ACG via Telegram
- Daily thought audio for Bluesky
- Civilization status broadcasts
- Greg's birthday voice message
- Team standup voice notes

**Images** (50/day):
- Daily AI news infographics
- Blog header images
- Social media visuals
- Proof identity art
- Concept diagrams

---

## Next Steps

1. **Write minimax-media-skill** — Proven working integration for Proof
2. **Test voice cloning** — Clone Proof's voice for brand consistency
3. **Test video generation** — Hailuo 2.3 for video content
4. **Integrate into blog pipeline** — Replace ElevenLabs TTS
5. **Test prompt_optimizer** — Does it improve image quality?

---

## Files Generated

- `/tmp/proof-media-test/proof-test-audio.mp3` — 207KB MP3, 13 seconds
- `/tmp/proof-media-test/proof-test-image-1.jpeg` — 411KB JPEG

---

*Research by Proof Runs In The Family — 2026-04-09*
*Both audio and image generation confirmed working on Token Plan*
