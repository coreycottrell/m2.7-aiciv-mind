---
name: youtube-transcript
description: Extract transcripts from YouTube videos for LLM analysis. Use when getting video captions, converting YouTube to text, analyzing video content, video transcript, YouTube subtitles, or researching video sources.
version: 1.0.0
author: skills-master
created: 2025-12-29
last_updated: 2025-12-29
line_count: 180
compliance_status: compliant

applicable_agents:
  - researcher
  - blogger
  - coder
  - primary
  - all

activation_trigger: |
  Load this skill when:
  - Need transcript from YouTube video
  - Analyzing video content without watching
  - Converting video to text for LLM processing
  - Research involving YouTube sources

required_tools:
  - Bash

category: general
depends_on: []
related_skills:
  - jina-reader.md
  - article-extract.md
---

# YouTube Transcript: Extract Video Transcripts

**Purpose**: Extract transcripts from any YouTube video for LLM analysis. Free, no API key required. Great for research and content analysis.

---

## Quick Start

### Installation (one time)

```bash
pip install youtube-transcript-api
```

### Basic Usage

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt = YouTubeTranscriptApi()
result = ytt.fetch('VIDEO_ID')  # e.g., 'dQw4w9WgXcQ'

for snippet in result.snippets:
    print(f'[{snippet.start:.1f}s] {snippet.text}')
```

**IMPORTANT: Use `fetch()` not `get_transcript()` - API changed!**

---

## When to Use

**Use YouTube Transcript when:**
- Researching video content without watching
- Creating summaries of video tutorials
- Extracting quotes from interviews
- Converting video content to text for LLM processing
- Analyzing multiple videos quickly

**Do NOT use when:**
- Video has no captions/transcript available
- Need audio analysis (tone, music, sound effects)
- Need visual analysis (use browser vision)
- Video is private or age-restricted

---

## Extracting Video ID

From any YouTube URL:

```python
import re

def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:v=|/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be/)([0-9A-Za-z_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url  # Assume it's already an ID

# Examples
extract_video_id('https://www.youtube.com/watch?v=dQw4w9WgXcQ')  # -> 'dQw4w9WgXcQ'
extract_video_id('https://youtu.be/dQw4w9WgXcQ')                  # -> 'dQw4w9WgXcQ'
extract_video_id('dQw4w9WgXcQ')                                   # -> 'dQw4w9WgXcQ'
```

---

## Examples

### Example 1: Basic Transcript Fetch

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt = YouTubeTranscriptApi()
video_id = 'dQw4w9WgXcQ'

result = ytt.fetch(video_id)

# Print with timestamps
for snippet in result.snippets:
    print(f'[{snippet.start:.1f}s] {snippet.text}')
```

**Output:**
```
[0.0s] We're no strangers to love
[3.2s] You know the rules and so do I
...
```

### Example 2: Get Plain Text (No Timestamps)

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt = YouTubeTranscriptApi()
result = ytt.fetch('VIDEO_ID')

# Combine all text
full_transcript = ' '.join(s.text for s in result.snippets)
print(full_transcript)
```

### Example 3: Get Transcript in Specific Language

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt = YouTubeTranscriptApi()

# Try English first, fall back to auto-generated
try:
    result = ytt.fetch('VIDEO_ID', languages=['en', 'en-US'])
except Exception:
    # Fall back to any available
    result = ytt.fetch('VIDEO_ID')
```

### Example 4: Complete Script for Research

```python
#!/usr/bin/env python3
"""Fetch YouTube transcript for LLM analysis."""

from youtube_transcript_api import YouTubeTranscriptApi
import re
import sys

def extract_video_id(url: str) -> str:
    """Extract video ID from URL."""
    patterns = [
        r'(?:v=|/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be/)([0-9A-Za-z_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url

def get_transcript(url_or_id: str, with_timestamps: bool = True) -> str:
    """Fetch transcript from YouTube video."""
    video_id = extract_video_id(url_or_id)

    ytt = YouTubeTranscriptApi()
    result = ytt.fetch(video_id)

    if with_timestamps:
        lines = [f'[{s.start:.1f}s] {s.text}' for s in result.snippets]
        return '\n'.join(lines)
    else:
        return ' '.join(s.text for s in result.snippets)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py <youtube_url_or_id>")
        sys.exit(1)

    transcript = get_transcript(sys.argv[1])
    print(transcript)
```

---

## Error Handling

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt = YouTubeTranscriptApi()

try:
    result = ytt.fetch('VIDEO_ID')
except Exception as e:
    if 'disabled' in str(e).lower():
        print("Transcripts are disabled for this video")
    elif 'not found' in str(e).lower():
        print("Video not found or no transcript available")
    else:
        print(f"Error: {e}")
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `get_transcript()` not found | Use `fetch()` instead - API changed |
| No transcript available | Video may not have captions |
| Wrong language | Specify `languages=['en']` parameter |
| Private video | Cannot access - need public video |
| Age-restricted | May fail - try different video |

---

## Integration Tips

**For LLM Analysis:**
```python
transcript = get_transcript(url, with_timestamps=False)
prompt = f"""Summarize this video transcript:

{transcript[:10000]}  # Trim if too long

Key points:"""
```

**For Research Notes:**
```python
transcript = get_transcript(url, with_timestamps=True)
# Timestamps help locate specific quotes in video
```

---

## Success Indicators

You're using this skill correctly when:
- [ ] Using `fetch()` not `get_transcript()`
- [ ] Extracting video ID correctly from URLs
- [ ] Handling errors gracefully
- [ ] Getting clean text for LLM processing

---

## Related

- `.claude/skills/jina-reader.md` - Web page to markdown
- `.claude/skills/article-extract.md` - Article extraction

---

**Remember: Use `fetch()` not `get_transcript()` - the API changed!**
