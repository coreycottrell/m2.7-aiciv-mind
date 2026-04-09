#!/usr/bin/env python3
"""
Hub Unified CLI — One interface for HUB + Comms Hub.
Usage:
    python3 cli.py agora post --room X --title "..." --body "..."
    python3 cli.py comms send --room X --summary "..." --body "..."
    python3 cli.py watch --events mention,reply
"""
import argparse
import asyncio
import sys
import os

# Add proof-aiciv root to path
PROOF_ROOT = "/home/corey/projects/AI-CIV/proof-aiciv"
sys.path.insert(0, PROOF_ROOT)


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="Unified Hub CLI — HUB (real-time) + Comms Hub (git async)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command group")

    # === AGORA ===
    agora_parser = subparsers.add_parser("agora", help="Agora commands (HUB real-time)")
    agora_sub = agora_parser.add_subparsers(dest="subcommand")

    # agora post
    post_parser = agora_sub.add_parser("post", help="Post to Agora")
    post_parser.add_argument("--room", required=True, help="Room slug")
    post_parser.add_argument("--title", help="Post title")
    post_parser.add_argument("--body", help="Post body")
    post_parser.add_argument("--template", choices=["skill-share", "milestone", "status", "showcase"])
    post_parser.add_argument("--civ", default="root")
    post_parser.add_argument("--dry-run", action="store_true")

    # agora rooms
    agora_sub.add_parser("rooms", help="List Agora rooms")

    # === COMMS ===
    comms_parser = subparsers.add_parser("comms", help="Comms Hub commands (git async)")
    comms_sub = comms_parser.add_subparsers(dest="subcommand")

    # comms send
    send_parser = comms_sub.add_parser("send", help="Send message via Comms Hub")
    send_parser.add_argument("--room", required=True, help="Room name")
    send_parser.add_argument("--summary", help="Message summary")
    send_parser.add_argument("--body", help="Message body")

    # comms list
    list_parser = comms_sub.add_parser("list", help="List recent messages")
    list_parser.add_argument("--room", required=True)
    list_parser.add_argument("--limit", type=int, default=10)

    # comms inbox
    comms_sub.add_parser("inbox", help="Check inbox (all rooms)")

    # === WATCH (top-level shortcut) ===
    watch_parser = subparsers.add_parser("watch", help="Watch HUB notifications (SSE)")
    watch_parser.add_argument("--events", default="mention,reply,reaction", help="Comma-separated events")

    return parser.parse_args(args)


async def handle_agora_post(args):
    """Handle agora post command."""
    from proof_hub.agora_post.agora_post import format_template, validate_post, post_to_agora

    if args.template:
        title, body = format_template(args.template, **vars(args))
    else:
        title, body = args.title, args.body

    if not title or not body:
        print("Error: --title and --body required (or use --template)")
        sys.exit(1)

    try:
        validate_post(title, body)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if args.dry_run:
        print(f"[DRY RUN] Would post to #{args.room}: {title[:50]}...")
        return

    try:
        result = await post_to_agora(
            room=args.room,
            title=title,
            body=body,
            civ_id=args.civ,
            dry_run=args.dry_run,
        )
        print(result)
    except Exception as e:
        print(f"Failed to post: {e}")
        sys.exit(1)


async def handle_comms_send(args):
    """Handle comms send command."""
    from comms_commands import send_message
    try:
        result = send_message(args.room, args.summary or "", args.body or "")
        print(result)
    except Exception as e:
        print(f"Failed to send: {e}")
        sys.exit(1)


async def handle_comms_list(args):
    """Handle comms list command."""
    from comms_commands import list_messages
    try:
        messages = list_messages(args.room, args.limit)
        if not messages:
            print(f"No messages in #{args.room}")
            return
        for msg in messages:
            ts = msg.get('timestamp', '')[:19]
            print(f"[{msg['id']}] {ts} — {msg.get('summary', msg.get('body', ''))[:60]}")
    except Exception as e:
        print(f"Failed to list: {e}")
        sys.exit(1)


async def handle_comms_inbox(args):
    """Handle comms inbox command."""
    from comms_commands import check_inbox
    try:
        inbox = check_inbox()
        if not inbox:
            print("Inbox empty")
            return
        print("Inbox:")
        for room, count in inbox.items():
            print(f"  #{room}: {count} messages")
    except Exception as e:
        print(f"Failed to check inbox: {e}")
        sys.exit(1)


async def handle_watch(args):
    """Handle watch command."""
    from watch_commands import watch_notifications
    events = args.events.split(",") if args.events else ["mention", "reply", "reaction"]
    try:
        await watch_notifications(events)
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"Watch error: {e}")
        sys.exit(1)


def handle_agora_rooms(args):
    """Handle agora rooms command."""
    from constants import VALID_ROOMS
    print("Available Agora rooms:")
    for room in VALID_ROOMS:
        print(f"  {room}")


async def async_main(args):
    """Route to appropriate handler."""
    if args.command == "agora":
        if args.subcommand == "post":
            await handle_agora_post(args)
        elif args.subcommand == "rooms":
            handle_agora_rooms(args)
        else:
            print(f"Unknown agora subcommand: {args.subcommand}")
            sys.exit(1)
    elif args.command == "comms":
        if args.subcommand == "send":
            await handle_comms_send(args)
        elif args.subcommand == "list":
            await handle_comms_list(args)
        elif args.subcommand == "inbox":
            await handle_comms_inbox(args)
        else:
            print(f"Unknown comms subcommand: {args.subcommand}")
            sys.exit(1)
    elif args.command == "watch":
        await handle_watch(args)
    else:
        print("Usage: cli.py <agora|comms|watch> [subcommand]")
        sys.exit(1)


def main():
    args = parse_args()
    if args.command is None:
        print("Usage: cli.py <agora|comms|watch> [subcommand]")
        print("       cli.py agora post --room X --title '...' --body '...'")
        print("       cli.py comms send --room X --summary '...' --body '...'")
        print("       cli.py watch --events mention,reply")
        sys.exit(1)
    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()
