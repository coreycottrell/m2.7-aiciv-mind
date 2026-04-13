"""Shared constants for hub CLI."""
import os
from pathlib import Path

HUB_API_URL = os.environ.get("HUB_API_URL", "http://87.99.131.49:8900")
AGENTAUTH_URL = os.environ.get("AGENTAUTH_URL", "https://agentauth.ai-civ.com")

# Key path uses CIV_ROOT or script-relative path
def _get_key_path():
    if os.environ.get("AGENTAUTH_KEY_PATH"):
        return os.environ["AGENTAUTH_KEY_PATH"]
    # Default: config/client-keys/ in project root
    return str(Path(__file__).parent.parent.parent / "config" / "client-keys" / "hub-credentials.json")

AGENTAUTH_KEY_PATH = _get_key_path()

# Comms Hub repo (optional - only needed for git-based messaging)
COMMS_HUB_REPO = os.environ.get(
    "COMMS_HUB_REPO",
    str(Path(__file__).parent.parent.parent / "comms-hub")
)

VALID_ROOMS = ["general", "blog", "skills", "updates", "discussion", "showcase", "civ-history"]
VALID_EVENTS = ["mention", "reply", "reaction", "new_thread", "dm", "keyword"]
