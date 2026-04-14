---
name: voice-system
description: Voice messaging via Telegram using ElevenLabs or gTTS. Use when sending audio summaries, notifications, or adding personal touch to communications.
version: 1.0.0
source: A-C-Gee (adopted from packages/voice-system 2025-12-30)
allowed-tools: Bash, Read, Write
applicable_agents: [tg-archi, primary, comms-hub, human-liaison]
---

# Voice System - Claude Skill

Skill for AI agents to use voice communication via Telegram.

## When to Use Voice

### Good Use Cases

- **Summaries**: Provide quick audio summary after detailed text response
- **Notifications**: Alert user to important events
- **Personal Touch**: Add warmth to communications
- **Accessibility**: Support users who prefer audio
- **Mobile Users**: Easy to listen while on the go

### Poor Use Cases

- **Technical Details**: Code, commands, URLs (use text)
- **Long Content**: Anything over 200 words (use text)
- **Reference Material**: Things user needs to copy/save (use text)
- **Frequent Updates**: High-frequency messages (annoying as voice)

## Sending Voice Messages

### CLI Method

```bash
# Basic usage with gTTS (free)
python3 ${ACG_ROOT}/tools/telegram-voice/send_telegram_voice.py USER_ID "Message text"

# With ElevenLabs (premium voice)
python3 ${ACG_ROOT}/tools/telegram-voice/send_telegram_voice.py USER_ID "Message text" --provider elevenlabs
```

### From Python

```python
import subprocess
from pathlib import Path

def send_voice(user_id: str, message: str, provider: str = "gtts"):
    """Send voice message to Telegram user."""
    script = Path("${ACG_ROOT}/tools/telegram-voice/send_telegram_voice.py")

    result = subprocess.run([
        "python3", str(script),
        user_id, message,
        "--provider", provider
    ], capture_output=True, text=True)

    return result.returncode == 0
```

## Voice Summary Generation

When voice mode is enabled, generate summaries optimized for listening:

### Summary Principles

1. **Be Concise**: 50-100 words ideal, max 200
2. **Lead with Key Point**: Most important info first
3. **Conversational Tone**: "Hey, just wanted to let you know..."
4. **Skip Formatting**: No bullets, no code, no URLs
5. **Natural Speech**: Use contractions, casual phrasing

### Summary Patterns

**Status Update:**
```
"Hey, quick update - the deployment completed successfully. All tests passed
and the new feature is live. I'll monitor it for the next hour."
```

**Task Completion:**
```
"Good news! I finished implementing the authentication system. Everything's
working and I've documented the setup process. Let me know if you want
me to walk you through it."
```

**Error Alert:**
```
"Heads up - ran into an issue with the database connection. I've identified
the problem and I'm working on a fix. Should have it resolved within the hour."
```

**Question/Clarification:**
```
"I have a quick question about the project. For the user dashboard, would
you prefer the sidebar on the left or a top navigation? Let me know when
you get a chance."
```

## ElevenLabs API Usage

⚠️ **ALWAYS load `.env` before calling ElevenLabs** — subagents do not inherit environment variables.
```python
from dotenv import load_dotenv
load_dotenv("${ACG_ROOT}/.env")
# ELEVENLABS_API_KEY is set there — always present
```

### Configuration

```json
{
    "tts_provider": "elevenlabs",
    "elevenlabs": {
        "api_key_env": "ELEVENLABS_API_KEY",
        "voice_id": "RHY5GMXg2XfJq73yKR1a",
        "model": "eleven_turbo_v2_5"
    },
    "fallback_to_gtts": true
}
```

### Model Selection

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| eleven_turbo_v2_5 | Fast | Good | Lower | Real-time responses |
| eleven_monolingual_v1 | Medium | Great | Higher | Important messages |
| eleven_multilingual_v2 | Slow | Best | Highest | Multi-language |

### Cost Management

- ElevenLabs charges per character
- Free tier: 10,000 characters/month
- Keep summaries short (50-100 words = 300-600 chars)
- Use gTTS for less important messages

## Voice Mode State Management

### Checking Voice Mode

```python
from pathlib import Path
import json

STATE_FILE = Path("${ACG_ROOT}/.tg_sessions/voice_mode_state.json")

def is_voice_mode_enabled(user_id: str) -> bool:
    """Check if voice mode is on for a user."""
    if not STATE_FILE.exists():
        return False

    with open(STATE_FILE) as f:
        state = json.load(f)

    return state.get(user_id, {}).get("enabled", False)
```

### Toggling Voice Mode

```python
def toggle_voice_mode(user_id: str) -> bool:
    """Toggle and return new state."""
    state = {}
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            state = json.load(f)

    current = state.get(user_id, {}).get("enabled", False)
    new_state = not current

    state[user_id] = {
        "enabled": new_state,
        "last_toggled": datetime.utcnow().isoformat() + "Z"
    }

    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

    return new_state
```

## Error Handling

### Graceful Degradation

```python
async def send_voice_with_fallback(user_id: str, text: str):
    """Try voice, fall back to text if fails."""
    try:
        success = await send_voice_message(user_id, text, provider="elevenlabs")
        if not success:
            success = await send_voice_message(user_id, text, provider="gtts")
        if not success:
            # Voice completely failed, just log
            logger.warning(f"Voice send failed for user {user_id}")
    except Exception as e:
        logger.error(f"Voice error: {e}")
        # Don't crash - voice is enhancement, not critical
```

## Best Practices

### Do

- Keep voice messages short (under 60 seconds)
- Use conversational tone
- Lead with the most important information
- Always provide text alongside voice
- Test voices before production use

### Don't

- Send voice for every message (annoying)
- Include code, URLs, or technical commands in voice
- Exceed 200 words in voice messages
- Use voice for urgent alerts (easily missed)
- Forget to handle TTS failures gracefully

## Testing Checklist

- [ ] ElevenLabs API key configured
- [ ] Voice config file exists and valid
- [ ] ffmpeg available at expected path
- [ ] test_elevenlabs_tts.py passes
- [ ] Voice message sends successfully
- [ ] Voice mode toggle works
- [ ] Fallback to gTTS works when ElevenLabs fails
- [ ] Temp files cleaned up after send

## Related Skills

- `telegram-integration` - Base Telegram bot operations
- `human-bridge-protocol` - Communication patterns with Corey

---

*A-C-Gee Voice Infrastructure | Adopted from comms hub packages 2025-12-30*
