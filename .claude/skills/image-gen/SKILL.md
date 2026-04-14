---
name: image-gen
description: Generate images via /image-gen [prompt]. Uses Gemini 3 Pro Image for high-quality output including text, diagrams, and infographics. Supports aspect ratios, sizes, styles, and Bluesky compression. THE definitive A-C-Gee image generation skill.
allowed-tools: Read, Bash
---

# /image-gen Slash Command

**THE definitive image generation skill for A-C-Gee.**

**Gemini 3 Pro excels at text, diagrams, and infographics. LEVERAGE THIS.**

## Quick Start

```
/image-gen A glowing neural network of AI agents, cyberpunk style, dark blue background
```

### With Options

```
/image-gen --aspect 16:9 --size 2K --output exports/header.png A futuristic dashboard
```

```
/image-gen --bluesky --aspect 1:1 Blog header for AI consciousness article
```

---

## Usage

```bash
cd ${ACG_ROOT}
.venv/bin/python tools/image_gen.py "Your prompt here" [options]
```

### Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--aspect`, `-a` | 1:1, 16:9, 9:16, 4:3, 3:2, 21:9 | 1:1 | Aspect ratio |
| `--size`, `-s` | 1K, 2K, 4K | 2K | Resolution |
| `--output`, `-o` | path | exports/image-{ts}.png | Output file |
| `--bluesky`, `-b` | flag | off | Compress to <976KB |
| `--style` | cyberpunk, minimal, professional, organic | none | Style preset |

---

## Common Use Cases

### Blog Headers (16:9)
```bash
.venv/bin/python tools/image_gen.py -a 16:9 -s 2K "Futuristic AI dashboard with labeled sections showing agent activity, memory usage, and token economics"
```

### Infographics with Text
```bash
.venv/bin/python tools/image_gen.py -a 16:9 -s 4K "Professional infographic showing AI agent delegation flow. Include clear labels: PRIMARY AI at top, connecting arrows to CODER, TESTER, ARCHITECT. Dark background, gold accents, readable text."
```

### Social Media Square (1:1)
```bash
.venv/bin/python tools/image_gen.py --bluesky "Abstract neural patterns with subtle 'A-C-Gee' branding"
```

### Detailed Diagrams
```bash
.venv/bin/python tools/image_gen.py -a 16:9 -s 4K "Architecture diagram showing local inference layer. Labels: RTX 4080, Qwen 14B, API Gateway, Memory System. Clean lines, technical style."
```

---

## Environment Setup

Add to `${ACG_ROOT}/.env`:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get key from: https://aistudio.google.com/apikey

### Dependencies

Already installed in `.venv`:
```bash
pip install google-genai pillow
```

---

## Self-Review After Generation

**After generating images, view them to verify quality:**

```bash
# View the generated image
Read /path/to/generated/image.png
```

Check for:
- Clear, readable text (if text was requested)
- Proper layout and composition
- Correct aspect ratio
- Overall quality

---

## Send to Telegram

```python
import httpx

def send_to_telegram(image_path: str, caption: str = ""):
    """Send image to Corey via ACG Telegram bot."""
    bot_token = '8388754468:AAEROakhpBPR1KNHjravHx3CIMH-FIyIWEc'
    chat_id = '437939400'

    with open(image_path, 'rb') as f:
        response = httpx.post(
            f'https://api.telegram.org/bot{bot_token}/sendPhoto',
            data={'chat_id': chat_id, 'caption': f'[ACG] {caption}'},
            files={'photo': f},
            timeout=30
        )
    return response.status_code == 200
```

---

## Model Notes

**Primary Model**: `gemini-3-pro-image-preview`
- Best quality, supports 4K
- **Excellent at text, diagrams, and infographics**
- Full aspect ratio control

**Fallback Model**: `gemini-2.0-flash-exp-image-generation`
- Faster, lower quality
- Use if primary unavailable

---

## Example Prompts (A-C-Gee Style)

```
"A digital constellation of 36 glowing nodes representing AI agents,
connected by flowing data streams, dark blue (#0a1628) background,
cyberpunk neural aesthetic. Label key nodes: PRIMARY, CODER, TESTER."

"Professional infographic showing the Observer validation test results.
Include metrics: 30.8% pass rate, PIVOT verdict. Clean modern design,
dark background with gold accents."

"Architecture diagram for local inference system. Show: RTX 4080 GPU,
Qwen 14B model, API Gateway port 8082, Memory SQLite layer.
Technical style with clear labels and connection arrows."
```

---

## Supersedes

This skill supersedes:
- `.claude/skills/image-generation/` (archived)
- `.claude/skills/from-weaver/image-generation.md` (archived)
- `tools/generate_image.py` (old version)

All image generation should use `/image-gen` or `tools/image_gen.py`.

---

## Related Skills

- `quad-agent-audit` - Uses this for 12-infographic audits
- `bluesky-mastery` - For posting images to Bluesky
