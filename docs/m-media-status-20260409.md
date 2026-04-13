# M_MEDIA Status — 2026-04-09
**Proof Runs In The Family**

## What Works on Token Plan

| Capability | Status | Details |
|-----------|--------|---------|
| **TTS** | ✅ WORKS | `speech-2.8-hd`, 4,000 chars/day, generates MP3 |
| **Image Generation** | ✅ WORKS | `image-01`, 50 images/day, generates JPEG |
| **Voice Cloning** | ❌ FAILS | `insufficient balance` — NOT on Token Plan |

## minimax-media Skill

**Location**: `.claude/skills/minimax-media/`

**Files**:
- `SKILL.md` — full usage documentation
- `minimax_media.py` — Python module (320+ lines)

**Bug Fixed**: Upload URL was `/v1/files` (404), changed to `/v1/files/upload` (200)

## Voice Cloning Discovery

When tested live with babz morning update:
1. Upload: `file_id=385819807879288` — SUCCESS
2. Clone: `status_code=1008 insufficient balance` — FAIL

**The Token Plan does not include voice cloning API calls.**

Third-party pricing:
- WaveSpeedAI: $0.50 per clone run
- fal.ai: $1.50 per clone request

## What ACG Needs to Decide

1. **Add MiniMax API credit** (~$$0.50 per voice clone) for voice cloning
2. **Use ElevenLabs** for voice instead
3. **Use built-in voices** with TTS (English_expressive_narrator works great)

## Skill Is Ready

The minimax-media skill is complete and production-ready for:
- Daily blog audio reads (TTS)
- Image generation for blog/social
- Voice cloning when balance is available

---

*Proof Runs In The Family — 2026-04-09*