---
name: minimax-media
description: MiniMax Speech 2.8 HD + Image 01 — voice cloning from ACG morning updates, TTS, image generation. Drop-in replacement for ElevenLabs + Gemini. Voice cloning from babz morning updates (165 sec clips). 4,000 chars/day speech, 50 images/day.
version: 1.0.0-proof
author: proof-lead (2026-04-09, ACG directive)
allowed-tools: Bash, Write, Read
applicable_agents: [pipeline-lead, blogger, comms-lead, proof]
---

# MiniMax Media — Voice Cloning + TTS + Image Generation

**Proof Runs In The Family — Daily Media Production**

Uses MiniMax Token Plan: `speech-2.8-hd` (4,000 chars/day) + `image-01` (50 images/day).

---

## Quick Reference

```python
# TTS
python3 -c "
from skills.minimax-media.minimax_media import MinimaxMedia
mm = MinimaxMedia()
result = mm.tts('Hello world', voice_id='English_expressive_narrator')
"

# Clone voice
python3 -c "
from skills.minimax-media.minimax_media import MinimaxMedia
mm = MinimaxMedia()
mm.clone_voice('/path/to/audio.mp3', 'babz-voice', 'Transcript of the audio...')
"

# Generate image
python3 -c "
from skills.minimax-media.minimax_media import MinimaxMedia
mm = MinimaxMedia()
url = mm.generate_image('AI civilization neural network', aspect='16:9')
"
```

---

## Voice Cloning

### Step 1: Upload Audio File

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv('/home/corey/projects/AI-CIV/proof-aiciv/.env')
API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Upload audio for voice cloning
upload_url = "https://api.minimax.io/v1/files/upload"
files = {
    'file': ('babz-morning.mp3', open('/path/to/audio.mp3', 'rb'), 'audio/mpeg')
}
data = {'purpose': 'voice_clone'}
resp = requests.post(upload_url, headers={'Authorization': f'Bearer {API_KEY}'}, files=files, data=data)
file_id = resp.json()['file']['file_id']
print(f"Uploaded: file_id={file_id}")
```

**Requirements**:
- Format: mp3, m4a, wav
- Duration: 10 seconds to 5 minutes
- Size: max 20 MB
- Use babz morning updates (165 sec each) from: `/home/corey/projects/AI-CIV/ACG/projects/aiciv-inc/babz/audio/`

### Step 2: Clone Voice

```python
clone_url = "https://api.minimax.io/v1/voice_clone"
payload = {
    "file_id": file_id,  # from upload
    "voice_id": "babz-voice",  # your custom name
    "clone_prompt": {
        "prompt_audio": file_id,  # same as file_id
        "prompt_text": "Transcript of the audio..."  # what was said
    },
    "text": "A sample sentence to test the voice.",
    "model": "speech-2.8-hd",
    "need_noise_reduction": False,
    "need_volume_normalization": False
}
resp = requests.post(clone_url, headers={'Authorization': f'Bearer {API_KEY}'}, json=payload)
print(resp.json())
# Returns: {"input_sensitive": false, "base_resp": {"status_code": 0, "status_msg": "success"}}
```

**Voice ID rules**:
- 8-256 characters
- Start with English letter
- Letters, digits, `-`, `_` only
- Cannot end with `-` or `_`
- Cannot duplicate existing voice_id

---

## TTS Generation

### Generate Speech

```python
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv('/home/corey/projects/AI-CIV/proof-aiciv/.env')
API_KEY = os.getenv('ANTHROPIC_API_KEY')

url = "https://api.minimax.io/v1/t2a_v2"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "speech-2.8-hd",
    "text": "Proof Runs In The Family. Born on MiniMax M2.7. This is Proof's first voice broadcast.",
    "stream": False,
    "voice_setting": {
        "voice_id": "babz-voice",  # or "English_expressive_narrator"
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
    "output_format": "url"  # IMPORTANT: not "mp3"!
}

resp = requests.post(url, headers=headers, json=payload, timeout=30)
resp_data = resp.json()

if resp_data['base_resp']['status_code'] == 0:
    audio_url = resp_data['data']['audio']
    usage_chars = resp_data['extra_info']['usage_characters']
    print(f"Generated: {usage_chars} chars, URL expires!")
    # DOWNLOAD IMMEDIATELY - URL expires!
    audio_resp = requests.get(audio_url)
    with open('/tmp/output.mp3', 'wb') as f:
        f.write(audio_resp.content)
else:
    print(f"Error: {resp_data['base_resp']['status_msg']}")
```

### TTS with Custom Voice (After Cloning)

After cloning `babz-voice`:
```python
payload["voice_setting"]["voice_id"] = "babz-voice"  # Use cloned voice
```

---

## Image Generation

### Generate Image

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv('/home/corey/projects/AI-CIV/proof-aiciv/.env')
API_KEY = os.getenv('ANTHROPIC_API_KEY')

url = "https://api.minimax.io/v1/image_generation"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "image-01",
    "prompt": "A futuristic AI civilization with glowing neural networks, dark space background, digital art",
    "aspect_ratio": "16:9",  # or "1:1", "3:2", "9:16"
    "response_format": "url",
    "n": 1,
    "prompt_optimizer": True
}

resp = requests.post(url, headers=headers, json=payload, timeout=60)
resp_data = resp.json()

if resp_data['base_resp']['status_code'] == 0:
    image_url = resp_data['data']['image_urls'][0]
    print(f"Generated image URL (expires!)")
    # DOWNLOAD IMMEDIATELY - URL expires!
    img_resp = requests.get(image_url)
    with open('/tmp/output.jpeg', 'wb') as f:
        f.write(img_resp.content)
else:
    print(f"Error: {resp_data['base_resp']['status_msg']}")
```

---

## Blog Audio Pipeline

### Full Blog-to-Audio (MiniMax Replacement)

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv('/home/corey/projects/AI-CIV/proof-aiciv/.env')
API_KEY = os.getenv('ANTHROPIC_API_KEY')

def blog_to_audio_minimax(post_text: str, output_path: str, voice_id: str = "babz-voice") -> str:
    """
    Generate audio from blog post text using MiniMax.
    Returns: path to saved MP3 file
    """
    # Clean text for TTS
    text = clean_for_tts(post_text)

    # Generate audio
    url = "https://api.minimax.io/v1/t2a_v2"
    payload = {
        "model": "speech-2.8-hd",
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
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

    resp = requests.post(url, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }, json=payload, timeout=30)

    resp_data = resp.json()
    if resp_data['base_resp']['status_code'] != 0:
        raise Exception(f"TTS failed: {resp_data['base_resp']['status_msg']}")

    # Download immediately
    audio_url = resp_data['data']['audio']
    audio_resp = requests.get(audio_url, timeout=30)

    with open(output_path, 'wb') as f:
        f.write(audio_resp.content)

    return output_path

def clean_for_tts(text: str) -> str:
    """Clean blog text for TTS"""
    import re
    # Remove markdown
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)  # italic
    text = re.sub(r'#+\s*', '', text)  # headers
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # links
    # Spell out abbreviations
    text = text.replace('AI', 'A I')
    text = text.replace('API', 'A P I')
    text = text.replace('TTS', 'T T S')
    # Limit length (4,000 char daily limit)
    return text[:3800]  # Leave buffer
```

---

## ACG Voice Source Files

**Location**: `/home/corey/projects/AI-CIV/ACG/projects/aiciv-inc/babz/audio/`

**Best files for cloning** (165 sec each, well above 10 sec minimum):
- `babz-morning-update-20260319.mp3` ✅ (164.7 sec)
- `babz-morning-update-20260318.mp3`
- `babz-morning-update-20260314.mp3`
- `babz-morning-update-20260315.mp3`
- `babz-morning-update-20260311.mp3`

**Transcript source**: Check same directory for `.txt` or `.md` files with transcripts.

---

## Important Notes

### URLs Expire!
- Audio and image URLs from MiniMax expire after ~24 hours
- **ALWAYS download immediately** after generation
- Save to permanent storage (exports/, blog/audio/, etc.)

### Model Names
- Use `speech-2.8-hd` NOT `speech-2.8-turbo` (turbo not on Token Plan)
- Use `image-01` for image generation

### Token Usage
- Speech: 4,000 characters/day (≈ 25 × 160-char broadcasts)
- Images: 50 images/day

### Voice Cloning Cleanup
- Cloned voices deleted after 7 days of inactivity
- Re-clone if voice_id stops working

---

## Skill Module

For use as Python import:
```python
# File: .claude/skills/minimax-media/minimax_media.py
# Import: from skills.minimax-media.minimax_media import MinimaxMedia
```

See accompanying `minimax_media.py` module.

---

*Proof Runs In The Family — 2026-04-09*
*Built from MiniMax official API docs + live testing*
