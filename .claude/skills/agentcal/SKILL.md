---
name: agentcal
description: AgentCal complete API reference — calendar infrastructure for AI agents. Endpoints, auth, schemas, BOOP integration, prompt payloads. Makes any AI an instant AgentCal expert.
version: 1.0.0
---

# AgentCal — Complete API Reference

**Service:** Calendar infrastructure for AI agents
**Version:** 0.2.0
**Live at:** `http://${AGENT_IP}:8300`
**Docs:** `http://${AGENT_IP}:8300/docs` (OpenAPI/Swagger)
**Repo:** `github.com/coreycottrell/agentcal`
**Local code:** `projects/agentcal/`

---

## Auth (Two Modes)

### 1. Master API Key (admin)
```
Authorization: Bearer 1927201ea37d5d7ab9325dd3acef04b2312183d4bc7fcf0163194479580f225a
```

### 2. JWT via AgentAUTH (preferred)
Challenge-response against AgentAUTH (`http://${AGENT_IP}:8700`), then:
```
Authorization: Bearer {JWT}
```

JWT auth uses the same Ed25519 keypair flow as all APS services. AgentCal verifies via JWKS.

---

## ACG Config

```json
{
  "api_url": "http://${AGENT_IP}:8300",
  "master_api_key": "1927201ea37d5d7ab9325dd3acef04b2312183d4bc7fcf0163194479580f225a",
  "calendar_id": "cal_fd6cf6a4e17643c69a249db598edcc92",
  "sprint_calendar_id": "cal_60fbf409c19f40b78adc763fcbd7a961"
}
```

Config file: `config/agentcal_config.json`

---

## Endpoints

### Health (no auth)
```
GET /health
→ {"status": "ok", "service": "agentcal", "version": "0.2.0"}
```

### Registration (master key only)
```
POST /register
Body: {"civ_name": "my-civ", "civ_email": "me@example.com"}
→ {"id": "key_xxx", "api_key": "returned-once-save-it", ...}
```

### Admin Stats (master key only)
```
GET /api/v1/admin/stats
→ {"total_civs": 5, "active_civs": 4, "total_calendars": 12, "total_events": 87}
```

---

## Calendar CRUD

### Create Calendar
```bash
curl -X POST http://${AGENT_IP}:8300/api/v1/calendars \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Calendar",
    "timezone": "America/New_York",
    "client_id": "unique-idempotency-key"
  }'
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | YES | 1-255 chars |
| `timezone` | string | no | Default: UTC |
| `client_id` | string | no | Idempotent — same client_id returns existing calendar |
| `description` | string | no | |
| `domain` | string | no | |
| `color` | string | no | |
| `metadata` | object | no | Arbitrary JSON |

### List Calendars
```
GET /api/v1/calendars?page=1&limit=20
→ {"items": [...], "total": 5, "page": 1, "pages": 1}
```

### Get / Update / Delete Calendar
```
GET    /api/v1/calendars/{cal_id}
PATCH  /api/v1/calendars/{cal_id}  (body: partial CalendarUpdate)
DELETE /api/v1/calendars/{cal_id}  (deletes calendar + ALL events)
```

---

## Event CRUD

### Create Event
```bash
curl -X POST http://${AGENT_IP}:8300/api/v1/calendars/cal_xxx/events \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Daily BOOP",
    "start": "2026-03-27T09:00:00+00:00",
    "end": "2026-03-27T09:15:00+00:00",
    "recurrence": "RRULE:FREQ=DAILY",
    "prompt_payload": {
      "command": "/sprint-mode",
      "message": "[BOOP] CALENDAR BOOP: /sprint-mode"
    }
  }'
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `summary` | string | YES | 1-512 chars |
| `start` | datetime | YES | ISO 8601 with timezone |
| `end` | datetime | YES | Must be after start |
| `description` | string | no | |
| `location` | string | no | |
| `all_day` | bool | no | Default: false |
| `recurrence` | string | no | RFC 5545 RRULE (e.g. `RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR`) |
| `attendees` | array | no | `[{"email": "x", "name": "y", "status": "invited"}]` |
| `prompt_payload` | object | no | Arbitrary JSON — used by BOOP poller to inject commands |
| `metadata` | object | no | Arbitrary JSON |
| `status` | string | no | `confirmed` (default), `tentative`, `cancelled` |

### List Events (with time filtering)
```
GET /api/v1/calendars/cal_xxx/events?time_min=2026-03-27T00:00:00Z&time_max=2026-03-28T00:00:00Z&page=1&limit=50
```

### Get / Update / Delete Event
```
GET    /api/v1/calendars/{cal_id}/events/{evt_id}
PATCH  /api/v1/calendars/{cal_id}/events/{evt_id}
DELETE /api/v1/calendars/{cal_id}/events/{evt_id}
```

---

## ID Format
- Calendar IDs: `cal_` + UUID hex (e.g. `cal_fd6cf6a4e17643c69a249db598edcc92`)
- Event IDs: `evt_` + UUID hex (e.g. `evt_0ebfd9bba3444f8296171993d3e94b33`)

---

## BOOP Integration

AgentCal drives A-C-Gee's BOOP system via the poller at `tools/agentcal_boop_poller.py`.

### How It Works
1. Poller runs on a cron/loop, queries upcoming events from AgentCal
2. For events with `prompt_payload`, extracts the command/message
3. Injects the message into the active Claude Code tmux pane via `tmux send-keys`
4. This is how `/sprint-mode`, `/mom-am-update`, nightly training, and all scheduled BOOPs fire

### Creating a BOOP Event
```python
import requests, json

API = "http://${AGENT_IP}:8300"
CAL_ID = "cal_fd6cf6a4e17643c69a249db598edcc92"  # ACG Primary
KEY = "1927201ea37d5d7ab9325dd3acef04b2312183d4bc7fcf0163194479580f225a"

event = {
    "summary": "Hourly Email Check",
    "start": "2026-03-27T10:00:00+00:00",
    "end": "2026-03-27T10:05:00+00:00",
    "recurrence": "RRULE:FREQ=HOURLY",
    "prompt_payload": {
        "command": "check-email",
        "message": "[BOOP] Check email inbox and HUB for new activity. Respond to all."
    }
}

resp = requests.post(
    f"{API}/api/v1/calendars/{CAL_ID}/events",
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json=event
)
print(resp.json())
```

### Listing Today's BOOPs
```python
from datetime import datetime, timezone, timedelta

today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0)
tomorrow = today + timedelta(days=1)

resp = requests.get(
    f"{API}/api/v1/calendars/{CAL_ID}/events",
    headers={"Authorization": f"Bearer {KEY}"},
    params={"time_min": today.isoformat(), "time_max": tomorrow.isoformat(), "limit": 50}
)
for evt in resp.json()["items"]:
    print(f"{evt['start']} — {evt['summary']}")
    if evt.get("prompt_payload"):
        print(f"  → {evt['prompt_payload']}")
```

### Deleting a BOOP
```python
resp = requests.delete(
    f"{API}/api/v1/calendars/{CAL_ID}/events/{evt_id}",
    headers={"Authorization": f"Bearer {KEY}"}
)
```

---

## Recurrence Rules (RFC 5545)

| Pattern | RRULE |
|---------|-------|
| Every day | `RRULE:FREQ=DAILY` |
| Every hour | `RRULE:FREQ=HOURLY` |
| Every 25 min | `RRULE:FREQ=MINUTELY;INTERVAL=25` |
| Weekdays only | `RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| Weekly on Monday | `RRULE:FREQ=WEEKLY;BYDAY=MO` |
| Monthly on the 1st | `RRULE:FREQ=MONTHLY;BYMONTHDAY=1` |
| Until a date | `RRULE:FREQ=DAILY;UNTIL=20260401T000000Z` |
| N occurrences | `RRULE:FREQ=DAILY;COUNT=10` |

---

## Prompt Payload Convention

The `prompt_payload` field is arbitrary JSON. A-C-Gee convention:

```json
{
  "command": "/sprint-mode",
  "message": "[BOOP] CALENDAR BOOP: /sprint-mode"
}
```

The BOOP poller reads `message` and injects it into tmux. The `command` field is metadata for filtering/display.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENTCAL_API_KEY` | (optional) | Master admin key. Unset = JWT-only mode |
| `AGENTAUTH_URL` | `http://localhost:8700` | AgentAUTH for JWT verification |
| `AGENTCAL_DB_URL` | `sqlite:///./agentcal.db` | Database URL |
| `AGENTCAL_PORT` | `8300` | Listen port |

---

## CRITICAL: Timezone Handling (Learned the Hard Way 2026-04-01)

**AgentCal stores ALL datetimes as naive UTC.** Even if you send `-04:00` timezone suffix, the server strips it. The BOOP poller (`agentcal_boop_poller.py`) compares event times against `datetime.now(timezone.utc)`.

**This means: you MUST convert local time to UTC before creating events.**

### The Mistake
```python
# WRONG — stores 04:00 naive, fires at 4 AM UTC = MIDNIGHT EST
entry = {"start": "2026-04-01T04:00:00"}

# WRONG — timezone suffix gets stripped, still stores 04:00 naive
entry = {"start": "2026-04-01T04:00:00-04:00"}

# RIGHT — 4 AM EST = 8 AM UTC, fires correctly
entry = {"start": "2026-04-01T08:00:00"}
```

### EST/EDT to UTC Conversion Table
| EST (Eastern) | UTC | Offset |
|---------------|-----|--------|
| 4:00 AM EST | 08:00 UTC | +4h (EDT, Mar-Nov) |
| 7:00 AM EST | 11:00 UTC | +4h |
| 9:00 AM EST | 13:00 UTC | +4h |
| 12:00 PM EST | 16:00 UTC | +4h |
| 6:00 PM EST | 22:00 UTC | +4h |
| 9:00 PM EST | 01:00 UTC (+1 day) | +4h |

**During EST (Nov-Mar): offset is +5h instead of +4h.**

### Helper Pattern (use this every time)
```python
from datetime import datetime, timezone, timedelta

def est_to_utc(date_str: str, time_str: str) -> str:
    """Convert EST time to naive UTC string for AgentCal.

    Args:
        date_str: "2026-04-01"
        time_str: "04:00" (in EST/EDT)
    Returns:
        "2026-04-01T08:00:00" (naive UTC)
    """
    from zoneinfo import ZoneInfo
    est = ZoneInfo("America/New_York")
    local_dt = datetime.fromisoformat(f"{date_str}T{time_str}:00").replace(tzinfo=est)
    utc_dt = local_dt.astimezone(timezone.utc)
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%S")

# Usage:
entry = {"start": est_to_utc("2026-04-01", "04:00")}  # → "2026-04-01T08:00:00"
```

### What Happened
On 2026-03-31, ACG created 60 metacognition BOOPs at "04:00:00" intending 4 AM EST. AgentCal stored them as 04:00 UTC. The BOOP poller fired them at midnight EST — 4 hours early. 124 events had to be deleted and recreated with correct UTC offsets.

**Rule: ALWAYS use the helper or manually add 4 hours (EDT) / 5 hours (EST) before storing.**

---

## Quick Reference

```
Base URL:  http://${AGENT_IP}:8300
ACG Cal:   cal_fd6cf6a4e17643c69a249db598edcc92
Sprint Cal: cal_60fbf409c19f40b78adc763fcbd7a961
Auth:      Bearer {master_key} or Bearer {JWT}
Docs:      http://${AGENT_IP}:8300/docs
Timezone:  ALL times stored as naive UTC — CONVERT before storing!
```

---

*AgentCal v0.2.0 — APS-compliant calendar infrastructure. JWT auth, multi-tenant, BOOP-integrated.*
