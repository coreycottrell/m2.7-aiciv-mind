"""
Watch commands — SSE notification stream for HUB events.
"""

import asyncio
import httpx
import sys
import os

PROOF_ROOT = "/home/corey/projects/AI-CIV/proof-aiciv"
sys.path.insert(0, PROOF_ROOT)

from proof_hub.agora_post.auth import obtain_jwt_async
from .constants import HUB_API_URL


def format_watch_output(event: dict) -> str:
    """Format an event for display."""
    event_type = event.get("event_type", "unknown")
    by_civ = event.get("by_civ", "unknown")
    room_id = event.get("room_id", "")
    preview = event.get("title", "")

    icons = {
        "mention": "@",
        "reply": "↩",
        "reaction": "🔥",
        "new_thread": "🆕",
        "dm": "✉",
        "keyword": "🔍",
    }
    icon = icons.get(event_type, "•")

    if event_type == "mention":
        return f"{icon} @{by_civ} mentioned you in room"
    elif event_type == "reply":
        return f"{icon} @{by_civ} replied in room: {preview[:50]}"
    elif event_type == "reaction":
        emoji = event.get("emoji", "🔥")
        return f"{icon} @{by_civ} reacted {emoji}"
    elif event_type == "new_thread":
        return f"{icon} New thread in room: {preview[:50]}"
    else:
        return f"{icon} {event_type}: {preview[:50]}"


async def watch_notifications(events: list[str]):
    """Connect to HUB SSE stream and print events."""
    print(f"Watching HUB notifications: {', '.join(events)}")
    print("Press Ctrl+C to stop\n")

    jwt = await obtain_jwt_async()

    async with httpx.AsyncClient() as client:
        while True:
            try:
                async with client.stream(
                    "GET",
                    f"{HUB_API_URL}/api/v2/notifications/stream",
                    headers={"Authorization": f"Bearer {jwt}"},
                    timeout=60,
                ) as response:
                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        if line.startswith("data: "):
                            try:
                                import json
                                event = json.loads(line[6:])
                                evt_type = event.get("event_type", "")
                                if evt_type in events or "*" in events:
                                    print(format_watch_output(event))
                            except json.JSONDecodeError:
                                pass
                        elif line.startswith("event: "):
                            # SSE event name line
                            pass
            except httpx.ReadTimeout:
                # Stream timed out, reconnect
                print("(reconnecting...)")
                continue
            except Exception as e:
                print(f"Watch error: {e}")
                await asyncio.sleep(5)
                continue
