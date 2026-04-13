"""
Comms Hub commands — git-based async messaging via comms-hub repo.
"""

import os
import json
import subprocess
import uuid
from pathlib import Path
from datetime import datetime

from constants import COMMS_HUB_REPO


def _run_git(*args, cwd=None):
    """Run git command in comms-hub repo."""
    repo = os.environ.get("COMMS_HUB_REPO", COMMS_HUB_REPO)
    result = subprocess.run(
        ["git", *args],
        cwd=cwd or repo,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {result.stderr}")
    return result.stdout


def _get_messages_dir(room: str) -> Path:
    """Get messages directory for a room."""
    repo = os.environ.get("COMMS_HUB_REPO", COMMS_HUB_REPO)
    messages_dir = Path(repo) / "messages" / room
    messages_dir.mkdir(parents=True, exist_ok=True)
    return messages_dir


def send_message(room: str, summary: str = "", body: str = "") -> str:
    """Send a message to a Comms Hub room."""
    if not summary and not body:
        raise ValueError("Either --summary or --body is required")

    msg_id = str(uuid.uuid4())[:8]
    timestamp = datetime.utcnow().isoformat()

    message = {
        "id": msg_id,
        "timestamp": timestamp,
        "from": "proof",
        "room": room,
        "summary": summary or body[:80],
        "body": body,
        "read": False,
    }

    messages_dir = _get_messages_dir(room)
    msg_file = messages_dir / f"{msg_id}.json"
    msg_file.write_text(json.dumps(message, indent=2))

    # Commit to git
    try:
        _run_git("add", ".")
        _run_git("commit", "-m", f"proof → {room}: {message['summary'][:50]}")
    except RuntimeError:
        # Git might not be available or repo not initialized
        pass

    return f"Message {msg_id} sent to #{room}"


def list_messages(room: str, limit: int = 10):
    """List recent messages in a room."""
    messages_dir = _get_messages_dir(room)

    if not messages_dir.exists():
        return []

    msg_files = sorted(messages_dir.glob("*.json"), reverse=True)[:limit]
    messages = []
    for f in msg_files:
        try:
            msg = json.loads(f.read_text())
            messages.append(msg)
        except (json.JSONDecodeError, IOError):
            continue

    return messages


def check_inbox() -> dict:
    """Check inbox across all rooms. Returns {room: message_count}."""
    repo = os.environ.get("COMMS_HUB_REPO", COMMS_HUB_REPO)
    messages_dir = Path(repo) / "messages"

    if not messages_dir.exists():
        return {}

    inbox = {}
    for room_dir in messages_dir.iterdir():
        if room_dir.is_dir():
            count = len(list(room_dir.glob("*.json")))
            if count > 0:
                inbox[room_dir.name] = count

    return inbox


def read_message(room: str, msg_id: str) -> dict | None:
    """Read a specific message."""
    messages_dir = _get_messages_dir(room)
    msg_file = messages_dir / f"{msg_id}.json"

    if not msg_file.exists():
        return None

    message = json.loads(msg_file.read_text())

    # Mark as read
    message["read"] = True
    msg_file.write_text(json.dumps(message, indent=2))

    return message
