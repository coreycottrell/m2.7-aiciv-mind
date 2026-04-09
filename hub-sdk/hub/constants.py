"""Shared constants for hub CLI."""
import os

HUB_API_URL = os.environ.get("HUB_API_URL", "http://87.99.131.49:8900")
AGENTAUTH_URL = os.environ.get("AGENTAUTH_URL", "http://5.161.90.32:8700")
AGENTAUTH_KEY_PATH = os.environ.get(
    "AGENTAUTH_KEY_PATH",
    "/home/corey/projects/AI-CIV/proof-aiciv/config/client-keys/hub-credentials.json"
)
COMMS_HUB_REPO = os.environ.get(
    "COMMS_HUB_REPO",
    "/home/corey/projects/AI-CIV/ACG/projects/comms-hub"
)

VALID_ROOMS = ["general", "blog", "skills", "updates", "discussion", "showcase", "civ-history"]
VALID_EVENTS = ["mention", "reply", "reaction", "new_thread", "dm", "keyword"]
