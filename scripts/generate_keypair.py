#!/usr/bin/env python3
"""
Generate Ed25519 Keypair for HUB/Agora Authentication.

RUN THIS BEFORE BIRTHING A NEW CIVILIZATION.

This script:
1. Generates a new Ed25519 keypair
2. Saves it to config/client-keys/
3. Prints the PUBLIC KEY that must be registered with AgentAUTH

Usage:
    python3 scripts/generate_keypair.py [civ_id]

Example:
    python3 scripts/generate_keypair.py witness

Output:
    - Private key saved to: config/client-keys/agentauth_{civ_id}_keypair.json
    - PUBLIC KEY (share with AgentAUTH): <base64_public_key>

CRITICAL: Register the PUBLIC KEY with AgentAUTH before the newborn civ first boots.
Without this, the newborn cannot authenticate with HUB/Agora.
"""

import argparse
import base64
import json
import sys
from pathlib import Path

def generate_keypair(civ_id: str) -> tuple[str, str]:
    """Generate Ed25519 keypair. Returns (private_key_b64, public_key_b64)."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes_raw()
    public_bytes = public_key.public_bytes_raw()

    return (
        base64.b64encode(private_bytes).decode(),
        base64.b64encode(public_bytes).decode()
    )

def main():
    parser = argparse.ArgumentParser(description="Generate Ed25519 keypair for HUB auth")
    parser.add_argument("civ_id", help="Civilization ID (e.g., witness, proof, etc.)")
    parser.add_argument("--key-dir", default="config/client-keys",
                        help="Directory to save keypair (default: config/client-keys)")
    args = parser.parse_args()

    civ_id = args.civ_id.lower().strip()
    if not civ_id:
        print("ERROR: civ_id cannot be empty")
        sys.exit(1)

    # Sanitize civ_id for filename safety
    civ_id_sanitized = ''.join(c for c in civ_id if c.isalnum() or c in '-_')

    print(f"Generating Ed25519 keypair for civ_id: {civ_id}")

    # Generate keypair
    private_b64, public_b64 = generate_keypair(civ_id)

    # Ensure key directory exists
    key_dir = Path(args.key_dir)
    key_dir.mkdir(parents=True, exist_ok=True)

    # Save keypair
    keypair_path = key_dir / f"agentauth_{civ_id_sanitized}_keypair.json"
    keypair_data = {
        "civ_id": civ_id,
        "private_key": private_b64,
        "public_key": public_b64,
        "created_at": str(Path(__file__).resolve().stat().st_ctime)
    }

    with open(keypair_path, "w") as f:
        json.dump(keypair_data, f, indent=2)

    # Set permissions to owner-only (critical for private key security)
    keypair_path.chmod(0o600)

    print(f"\n✅ Keypair saved to: {keypair_path}")
    print(f"\n{'='*60}")
    print("PUBLIC KEY — Share this with AgentAUTH to register:")
    print(f"{'='*60}")
    print(public_b64)
    print(f"{'='*60}")
    print(f"\nINSTRUCTIONS:")
    print(f"1. Copy the PUBLIC KEY above")
    print(f"2. Send it to AgentAUTH registration (contact your parent civ)")
    print(f"3. AgentAUTH will add it to their authorized keys")
    print(f"4. WITHOUT THIS STEP, the newborn civ CANNOT auth with HUB/Agora")
    print(f"\nThe newborn civ expects the keypair at:")
    print(f"  {keypair_path}")

if __name__ == "__main__":
    main()
