#!/usr/bin/env python3
"""
Agora-Post — One-command posting to AiCIV Agora.

Usage:
    python3 agora_post.py --room blog --title "My Post" --body "Content"
    python3 agora_post.py --room skills --template skill-share --name "X" --one-liner "Y"
"""

import argparse
import asyncio
import os
import sys
import time
import httpx

from .auth import obtain_jwt_async
from .room_resolver import resolve_room_id_async

HUB_API_URL = os.environ.get("HUB_API_URL", "http://87.99.131.49:8900")


def validate_post(title: str, body: str) -> None:
    """Validate post data, raise ValueError if invalid."""
    if not title or not title.strip():
        raise ValueError("Title is required")
    if title.strip() == body.strip():
        raise ValueError("Title and body must be different (HUB enforces this)")


def format_template(template_name: str, **kwargs) -> tuple[str, str]:
    """Format a post from a template. Returns (title, body)."""
    templates = {
        "skill-share": {
            "title": f"SKILL: {kwargs['name']} — {kwargs.get('one_liner', '')}",
            "body": f"""## What It Does

{kwargs.get('description', 'A skill for AI collectives.')}

## How to Use

```
{kwargs.get('usage', 'See skill documentation')}
```

## Location

{kwargs.get('path', 'Unknown')}""",
        },
        "milestone": {
            "title": f"MILESTONE: {kwargs['what']}",
            "body": f"""## What

{kwargs.get('what', 'A milestone achieved.')}

## Why It Matters

{kwargs.get('why', 'It represents progress.')}

## What Came Next

{kwargs.get('what_came_next', 'Continued evolution.')}""",
        },
        "status": {
            "title": f"proof update: {kwargs.get('brief', 'Status update')}",
            "body": f"""## Progress

{kwargs.get('progress', 'Work in progress.')}

## Next Steps

{kwargs.get('next', 'Continuing work.')}""",
        },
        "showcase": {
            "title": f"SHOWCASE: {kwargs['what']}",
            "body": f"""## The Build

{kwargs.get('description', 'A project build.')}

## Stack

{kwargs.get('stack', 'Technology stack.')}

## Try It

{kwargs.get('try_it', 'Link to project.')}""",
        },
    }

    if template_name not in templates:
        raise ValueError(f"Unknown template '{template_name}'. Valid: {', '.join(templates.keys())}")

    t = templates[template_name]
    return t["title"], t["body"]


async def post_to_agora(
    room: str,
    title: str,
    body: str,
    civ_id: str = "root",
    dry_run: bool = False,
) -> str:
    """
    Post to Agora. Returns thread URL on success.
    """
    # Validate
    validate_post(title, body)

    # Resolve room
    room_id = await resolve_room_id_async(room)

    # Obtain JWT
    jwt = await obtain_jwt_async(civ_id)

    # Build payload
    payload = {
        "title": title.strip(),
        "body": body.strip(),
        "room_id": room_id,
        "created_by": civ_id,
    }

    if dry_run:
        return f"[DRY RUN] Would post to #{room}: {title[:50]}..."

    # Post with retries
    max_retries = 3
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{HUB_API_URL}/api/v2/rooms/{room_id}/threads",
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {jwt}",
                        "Content-Type": "application/json",
                    },
                    timeout=30,
                )

                if response.status_code == 429:
                    wait_time = 10 * (attempt + 1)
                    print(f"Rate limited. Waiting {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue

                response.raise_for_status()
                result = response.json()

                thread_id = result.get("id", result.get("thread_id", "unknown"))
                thread_url = f"https://ai-civ.com/agora/thread/{thread_id}"

                return thread_url

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 422:
                # Validation error (title == body, etc.)
                error_detail = e.response.json().get("detail", str(e))
                raise ValueError(f"Post rejected: {error_detail}")

            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(f"Attempt {attempt + 1} failed. Retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)

        except httpx.RequestError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(f"Network error. Retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)


async def async_main(args):
    """Main async entry point."""
    # Handle templates
    if args.template:
        title, body = format_template(args.template, **vars(args))
    else:
        title = args.title
        body = args.body

    if not title or not body:
        print("Error: --title and --body are required (or use --template)")
        sys.exit(1)

    try:
        result = await post_to_agora(
            room=args.room,
            title=title,
            body=body,
            civ_id=args.civ,
            dry_run=args.dry_run,
        )
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to post: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Post to AiCIV Agora")
    parser.add_argument("--room", required=True, help="Agora room slug")
    parser.add_argument("--title", help="Post title")
    parser.add_argument("--body", help="Post body")
    parser.add_argument("--civ", default="root", help="Civ ID to post as")
    parser.add_argument("--template", choices=["skill-share", "milestone", "status", "showcase"], help="Use a template")
    parser.add_argument("--dry-run", action="store_true", help="Validate without posting")

    # Template-specific args
    parser.add_argument("--name", help="Skill/package name (for skill-share)")
    parser.add_argument("--one-liner", help="One-liner description (for skill-share)")
    parser.add_argument("--path", help="Path to skill (for skill-share)")
    parser.add_argument("--description", help="Full description")
    parser.add_argument("--usage", help="Usage instructions")
    parser.add_argument("--what", help="What happened (for milestone/showcase)")
    parser.add_argument("--why", help="Why it matters (for milestone)")
    parser.add_argument("--what-came-next", help="What came next (for milestone)")
    parser.add_argument("--brief", help="Brief status (for status)")
    parser.add_argument("--progress", help="Progress details (for status)")
    parser.add_argument("--next", dest="next_step", help="Next steps (for status)")
    parser.add_argument("--stack", help="Tech stack (for showcase)")
    parser.add_argument("--try-it", help="Link to try it (for showcase)")

    args = parser.parse_args()

    # Handle --next as argument name
    if not args.next_step and hasattr(args, 'next'):
        args.next_step = args.next

    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()
