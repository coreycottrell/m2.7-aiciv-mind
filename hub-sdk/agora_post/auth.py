"""
JWT obtain and cache for Agora posting.
Uses Ed25519 challenge-response with AgentAUTH.
"""

import os
import time
import json
import base64
import hashlib
from pathlib import Path

try:
    from nacl.signing import SigningKey
    from nacl.encoding import RawEncoder
    HAS_NACL = True
except ImportError:
    HAS_NACL = False

import httpx

AGENTAUTH_URL = os.environ.get("AGENTAUTH_URL", "https://agentauth.ai-civ.com")
HUB_API_URL = os.environ.get("HUB_API_URL", "http://87.99.131.49:8900")
KEY_PATH = os.environ.get(
    "AGENTAUTH_KEY_PATH",
    str(Path(__file__).parent.parent.parent / "config" / "client-keys" / "hub-credentials.json")
)


class JWTCache:
    """Simple in-memory JWT cache."""

    def __init__(self):
        self._token = None
        self._expires_at = 0

    def set(self, token: str, expires_at: float):
        self._token = token
        self._expires_at = expires_at

    def get(self) -> str | None:
        if time.time() >= self._expires_at:
            return None
        return self._token

    @property
    def is_valid(self) -> bool:
        return self._token is not None and time.time() < self._expires_at


_jwt_cache_instance = JWTCache()


def _load_private_key() -> bytes:
    """Load Ed25519 private key from file (supports both raw binary and JSON formats)."""
    key_file = Path(KEY_PATH)
    if not key_file.exists():
        raise FileNotFoundError(f"Private key not found at {KEY_PATH}")

    content = key_file.read_text()

    # Check if it's JSON (hub-credentials.json format)
    if content.strip().startswith('{'):
        import json
        data = json.loads(content)
        priv_b64 = data.get('private_key') or data.get('private_key_b64')
        if not priv_b64:
            raise ValueError(f"No private_key in {KEY_PATH}")
        return base64.b64decode(priv_b64)

    # Raw binary file
    return content.encode('latin-1') if isinstance(content, str) else content


async def obtain_jwt_async(civ_id: str = "root") -> str:
    """Obtain JWT from AgentAUTH via Ed25519 challenge-response."""
    if _jwt_cache_instance.is_valid:
        return _jwt_cache_instance.get()

    async with httpx.AsyncClient() as client:
        # Step 1: Get challenge
        challenge_resp = await client.post(
            f"{AGENTAUTH_URL}/challenge",
            json={"civ_id": civ_id}
        )
        challenge_resp.raise_for_status()
        challenge_data = challenge_resp.json()
        challenge_b64 = challenge_data["challenge"]

        # Step 2: Sign the challenge
        challenge_bytes = base64.b64decode(challenge_b64)
        private_key_bytes = _load_private_key()

        if HAS_NACL:
            signing_key = SigningKey(private_key_bytes)
            signed = signing_key.sign(challenge_bytes, encoder=RawEncoder)
            signature_b64 = base64.b64encode(signed.signature).decode()
        else:
            # Fallback: manual Ed25519 sign using ed25519 Blake3 library
            import ed25519
            signing_key = ed25519.SigningKey(private_key_bytes)
            signed = signing_key.sign(challenge_bytes)
            signature_b64 = base64.b64encode(signed).decode()

        # Step 3: Verify and get JWT
        verify_resp = await client.post(
            f"{AGENTAUTH_URL}/verify",
            json={
                "civ_id": civ_id,
                "signature": signature_b64,
            }
        )
        verify_resp.raise_for_status()
        jwt = verify_resp.json()["token"]

        # Cache for 55 minutes (JWT TTL is 1 hour)
        _jwt_cache_instance.set(jwt, time.time() + 3300)
        return jwt


def get_jwt_sync(civ_id: str = "root") -> str:
    """Synchronous JWT obtain."""
    import asyncio
    return asyncio.run(obtain_jwt_async(civ_id))
