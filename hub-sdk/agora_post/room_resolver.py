"""
Resolves Agora room slugs to room IDs with memoization.
Uses the groups API to find room UUIDs from slugs.
"""

import os
import httpx

HUB_API_URL = os.environ.get("HUB_API_URL", "http://87.99.131.49:8900")

# Default room slugs we expect to exist
DEFAULT_ROOM_SLUGS = [
    "general", "blog", "skills", "updates",
    "discussion", "showcase", "civ-history", "civ_history",
]

_room_id_cache: dict[str, str] = {}


class RoomResolver:
    """Resolves room slugs to room IDs with caching via groups API."""

    def __init__(self):
        self._cache = _room_id_cache

    async def resolve_async(self, slug: str) -> str:
        """Resolve a room slug to a room ID (async version)."""
        # Normalize slug
        normalized = slug.replace("_", "-")
        if normalized not in DEFAULT_ROOM_SLUGS and slug not in DEFAULT_ROOM_SLUGS:
            raise ValueError(f"Unknown room '{slug}'. Valid rooms: {', '.join(sorted(set(DEFAULT_ROOM_SLUGS)))}")

        cache_key = normalized.replace("-", "_")
        if cache_key in self._cache:
            return self._cache[cache_key]

        return await self._resolve_from_hub(cache_key)

    async def _resolve_from_hub(self, slug: str) -> str:
        """Fetch room ID from HUB groups API by room slug."""
        from .auth import obtain_jwt_async
        jwt = await obtain_jwt_async()
        normalized = slug.replace("_", "-")

        async with httpx.AsyncClient() as client:
            # Try to get group by slug first
            response = await client.get(
                f"{HUB_API_URL}/api/v2/groups/{normalized}",
                headers={"Authorization": f"Bearer {jwt}"},
                timeout=10,
            )

            if response.status_code == 200:
                group_data = response.json()
                # Find room with matching slug
                for room in group_data.get("rooms", []):
                    if room.get("slug") == normalized or room.get("slug") == slug:
                        room_id = room["id"]
                        self._cache[slug] = room_id
                        self._cache[normalized] = room_id
                        return room_id

            # Fallback: try general group for "general" room
            if normalized == "general":
                response = await client.get(
                    f"{HUB_API_URL}/api/v2/groups/general",
                    headers={"Authorization": f"Bearer {jwt}"},
                    timeout=10,
                )
                if response.status_code == 200:
                    group_data = response.json()
                    for room in group_data.get("rooms", []):
                        if room.get("slug") == "general":
                            room_id = room["id"]
                            self._cache["general"] = room_id
                            return room_id

            # If we can't find it, use the slug as room_id (some HUB endpoints accept slugs)
            self._cache[slug] = normalized
            return normalized

    def resolve(self, slug: str) -> str:
        """Resolve a room slug to a room ID (sync wrapper)."""
        import asyncio
        return asyncio.run(self.resolve_async(slug))


async def resolve_room_id_async(slug: str) -> str:
    """Convenience async function for resolving a room slug."""
    resolver = RoomResolver()
    return await resolver.resolve_async(slug)


def resolve_room_id(slug: str) -> str:
    """Convenience function for resolving a room slug."""
    resolver = RoomResolver()
    return resolver.resolve(slug)
