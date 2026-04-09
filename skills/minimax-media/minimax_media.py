#!/usr/bin/env python3
"""
MiniMax Media — Voice Cloning + TTS + Image Generation
Proof Runs In The Family — 2026-04-09

Usage:
    from skills.minimax-media.minimax_media import MinimaxMedia
    mm = MinimaxMedia()
"""

import os
import re
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('/home/corey/projects/AI-CIV/proof-aiciv/.env')

API_KEY = os.getenv('ANTHROPIC_API_KEY')
BASE_URL = "https://api.minimax.io"


class MinimaxMedia:
    """MiniMax Media Production — Voice cloning, TTS, Image generation"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("No API key found. Set ANTHROPIC_API_KEY in .env")

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    # === VOICE CLONING ===

    def upload_audio(self, audio_path: str, purpose: str = "voice_clone") -> int:
        """
        Upload audio file for voice cloning.
        Returns: file_id (int)

        Requirements:
        - Format: mp3, m4a, wav
        - Duration: 10 seconds to 5 minutes
        - Size: max 20 MB
        """
        url = f"{BASE_URL}/v1/files/upload"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        with open(audio_path, 'rb') as f:
            files = {'file': (Path(audio_path).name, f, 'audio/mpeg')}
            data = {'purpose': purpose}
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=60)

        resp_data = resp.json()
        if resp.status_code != 200:
            raise Exception(f"Upload failed: {resp_data}")

        file_id = resp_data.get('id')
        print(f"Uploaded: file_id={file_id}")
        return file_id

    def clone_voice(
        self,
        audio_path: str,
        voice_id: str,
        prompt_text: str = None,
        model: str = "speech-2.8-hd"
    ) -> dict:
        """
        Clone a voice from an audio file.

        Args:
            audio_path: Path to MP3/WAV/M4A file (10 sec to 5 min)
            voice_id: Custom name for the voice (8-256 chars, starts with letter)
            prompt_text: Transcript of the audio (improves quality)
            model: Model to use (speech-2.8-hd recommended)
        """
        # Upload audio
        file_id = self.upload_audio(audio_path)

        # Clone voice
        url = f"{BASE_URL}/v1/voice_clone"
        payload = {
            "file_id": file_id,
            "voice_id": voice_id,
            "clone_prompt": {
                "prompt_audio": file_id,
                "prompt_text": prompt_text or "Transcript of the audio file."
            },
            "text": "A sample sentence to verify the voice.",
            "model": model,
            "need_noise_reduction": False,
            "need_volume_normalization": False
        }

        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp_data = resp.json()

        if resp_data['base_resp']['status_code'] != 0:
            raise Exception(f"Clone failed: {resp_data['base_resp']['status_msg']}")

        print(f"Voice cloned: {voice_id}")
        return resp_data

    def get_voices(self) -> list:
        """List all available voices for this account"""
        url = f"{BASE_URL}/v1/voice/get"
        resp = requests.post(url, headers=self._headers(), json={}, timeout=30)
        return resp.json().get('data', {}).get('voice_list', [])

    # === TTS ===

    def tts(
        self,
        text: str,
        voice_id: str = "English_expressive_narrator",
        speed: float = 1.0,
        output_path: str = None,
        model: str = "speech-2.8-hd"
    ) -> dict:
        """
        Generate speech from text.

        Returns: dict with 'path' (if output_path given), 'url' (expiring), 'usage_chars'
        """
        url = f"{BASE_URL}/v1/t2a_v2"
        payload = {
            "model": model,
            "text": text[:3800],  # Leave buffer under 4000 char limit
            "stream": False,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
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

        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp_data = resp.json()

        if resp_data['base_resp']['status_code'] != 0:
            raise Exception(f"TTS failed: {resp_data['base_resp']['status_msg']}")

        audio_url = resp_data['data']['audio']
        usage_chars = resp_data['extra_info']['usage_characters']

        result = {
            'url': audio_url,
            'usage_chars': usage_chars,
            'audio_length': resp_data['extra_info'].get('audio_length', 0)
        }

        # Download immediately if output_path given
        if output_path:
            audio_resp = requests.get(audio_url, timeout=30)
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(audio_resp.content)
            result['path'] = output_path

        return result

    # === IMAGE GENERATION ===

    def generate_image(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        output_path: str = None,
        model: str = "image-01",
        n: int = 1
    ) -> dict:
        """
        Generate image(s) from text prompt.

        Args:
            prompt: Image description
            aspect_ratio: "16:9", "1:1", "3:2", "9:16"
            output_path: Save path (downloads immediately)
            model: "image-01" recommended
            n: Number of images (1-4)
        """
        url = f"{BASE_URL}/v1/image_generation"
        payload = {
            "model": model,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "response_format": "url",
            "n": min(n, 4),
            "prompt_optimizer": True
        }

        resp = requests.post(url, headers=self._headers(), json=payload, timeout=60)
        resp_data = resp.json()

        if resp_data['base_resp']['status_code'] != 0:
            raise Exception(f"Image failed: {resp_data['base_resp']['status_msg']}")

        image_urls = resp_data['data']['image_urls']

        result = {'urls': image_urls}

        # Download immediately if output_path given
        if output_path:
            img_resp = requests.get(image_urls[0], timeout=30)
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(img_resp.content)
            result['path'] = output_path

        return result

    # === BLOG AUDIO PIPELINE ===

    def blog_to_audio(
        self,
        post_text: str,
        output_path: str,
        voice_id: str = "babz-voice"
    ) -> str:
        """
        Generate audio from blog post text.
        Returns: path to saved MP3 file

        Args:
            post_text: Raw blog post text (markdown stripped)
            output_path: Where to save the MP3
            voice_id: Voice to use
        """
        cleaned = self._clean_for_tts(post_text)
        result = self.tts(cleaned, voice_id=voice_id, output_path=output_path)
        return result['path']

    def _clean_for_tts(self, text: str) -> str:
        """Clean blog text for TTS"""
        # Remove markdown
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)  # italic
        text = re.sub(r'#+\s*', '', text)  # headers
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # links
        text = re.sub(r'\n{3,}', '\n\n', text)  # excessive newlines

        # Spell out abbreviations
        replacements = {
            'AI': 'A I',
            'API': 'A P I',
            'TTS': 'T T S',
            'URL': 'U R L',
            'HTML': 'H T M L',
            'CSS': 'C S S',
            'JSON': 'J S O N',
            'GPT': 'G P T',
            'LLM': 'L L M',
            'NLP': 'N L P',
            'PC': 'P C',
            'CEO': 'C E O',
            'CTO': 'C T O',
        }
        for abbr, spelled in replacements.items():
            text = text.replace(abbr, spelled)

        # Leave buffer under 4000 char limit
        return text[:3800]

    # === UTILITY ===

    def save_expiring_url(self, url: str, output_path: str) -> str:
        """Download expiring URL content to permanent storage"""
        resp = requests.get(url, timeout=30)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(resp.content)
        return output_path


if __name__ == "__main__":
    import sys

    mm = MinimaxMedia()

    if len(sys.argv) < 2:
        print("Usage: python3 minimax_media.py <tts|clone|image> [args...]")
        print("  tts <text> [voice_id] [output.mp3]")
        print("  image <prompt> [aspect] [output.jpg]")
        print("  clone <audio.mp3> <voice_id> [transcript]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "tts":
        text = sys.argv[2] if len(sys.argv) > 2 else "Hello from Proof Runs In The Family."
        voice_id = sys.argv[3] if len(sys.argv) > 3 else "English_expressive_narrator"
        output = sys.argv[4] if len(sys.argv) > 4 else "/tmp/proof-tts.mp3"
        result = mm.tts(text, voice_id=voice_id, output_path=output)
        print(f"TTS generated: {output}")
        print(f"Characters used: {result['usage_chars']}")

    elif cmd == "image":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "AI civilization neural network"
        aspect = sys.argv[3] if len(sys.argv) > 3 else "16:9"
        output = sys.argv[4] if len(sys.argv) > 4 else "/tmp/proof-image.jpg"
        result = mm.generate_image(prompt, aspect_ratio=aspect, output_path=output)
        print(f"Image generated: {output}")

    elif cmd == "clone":
        audio = sys.argv[2]
        voice_id = sys.argv[3]
        transcript = sys.argv[4] if len(sys.argv) > 4 else None
        result = mm.clone_voice(audio, voice_id, prompt_text=transcript)
        print(f"Voice '{voice_id}' cloned successfully")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
