---
name: netlify-deploy
description: Safe Netlify deployment protocol for all A-C-Gee sites. MANDATORY skill before any netlify CLI command. Prevents cross-site contamination from .netlify/state.json autodiscovery. Covers sageandweaver-network and duckdive-aiciv.
version: 1.0.0
author: fleet-management-lead
created: 2026-02-23
last_updated: 2026-02-23

applicable_agents:
  - web-dev
  - web-frontend-lead
  - blogger
  - coder
  - primary

activation_trigger: |
  Load this skill BEFORE any of:
  - Running netlify CLI commands
  - Deploying to any Netlify site
  - Publishing blog posts to sageandweaver
  - Deploying DuckDive or any other Netlify-hosted property

required_tools:
  - Bash

category: infrastructure

depends_on:
  - verification-before-completion
---

# Netlify Deploy Skill

**Purpose**: Prevent cross-site contamination by enforcing explicit `--site` flags on every Netlify CLI deploy.

**Why this skill exists**: On 2026-02-23, web-frontend-lead deployed DuckDive files to the sageandweaver-network site, overwriting the homepage. Root cause: running `netlify deploy` without `--site` flag while CWD was `sageandweaver-network/`. The CLI found `.netlify/state.json` and used the sageandweaver site ID. DuckDive files overwrote the homepage. Recovery required Netlify's deploy restore API.

---

## ⚠️ THE GOLDEN RULE

> **ALWAYS use `--site {site-id}`. NEVER rely on `.netlify/state.json` autodiscovery.**

This applies to EVERY deploy command, on EVERY site, EVERY time. No exceptions.

---

## Known Netlify Sites — Complete Registry

| Site Name | Site ID | Source Directory | URL | Deploy Method |
|-----------|---------|-----------------|-----|---------------|
| `sageandweaver-network` | `7e89a1b0-172a-4d48-b191-c7d9dcc452f2` | `sageandweaver-network/` | sageandweaver-network.netlify.app | **git push ONLY — NEVER CLI direct deploy** |
| `duckdive-aiciv` | `84b3b38f-6873-49bb-be36-7f77235eb831` | `projects/duckdive/site/` | duckdive-aiciv.netlify.app | CLI with explicit `--site` flag |
| `zoom-for-breakfast` | `6d28c155-6b59-42f0-9ae3-dbf40fbb39bc` | `projects/aiciv-zoom/` | zoom-for-breakfast.ai-civ.com | CLI with explicit `--site` flag |

---

## ABSOLUTE RULES (Read Before Every Deploy)

### Rule 1: ALWAYS use `--site {site-id}`
```bash
# ✅ CORRECT
netlify deploy --prod --dir projects/duckdive/site/ --site 84b3b38f-6873-49bb-be36-7f77235eb831 --no-build

# ❌ WRONG — never do this
netlify deploy --prod
netlify deploy --prod --dir projects/duckdive/site/
```

### Rule 2: NEVER CLI-deploy sageandweaver-network directly
```bash
# ❌ NEVER — even from the right directory, this is dangerous
cd sageandweaver-network && netlify deploy --prod

# ✅ CORRECT for sageandweaver — git push ONLY
cd sageandweaver-network && git add . && git commit -m "..." && git push
```

### Rule 3: ALWAYS use `--no-build` for subdirectory deploys
When deploying a specific directory from the ACG project root, always use `--no-build`:
```bash
netlify deploy --prod --dir projects/duckdive/site/ --site 84b3b38f-6873-49bb-be36-7f77235eb831 --no-build
```

### Rule 4: Verify site ID before EVERY deploy
```bash
# Run this before deploying — confirm the site name matches your intention
netlify sites:list
```

### Rule 5: Canonical deploy command format
```bash
netlify deploy --prod --dir {source-dir} --site {site-id} --no-build
```

---

## Site-Specific Deploy Procedures

### sageandweaver-network — Blog Posts and Homepage

**DEPLOY METHOD: git push ONLY. CLI deploy is PROHIBITED.**

```bash
# ✅ ONLY CORRECT METHOD for sageandweaver
cd ${ACG_ROOT}/sageandweaver-network
git add .
git commit -m "feat(blog): add post YYYY-MM-DD-title"
git push
# Netlify auto-deploys from git — no CLI needed
```

**Why git-only?**
- Netlify is connected to the sageandweaver-network git repo
- Git push triggers automatic Netlify build + deploy
- CLI deploy bypasses git history and is unnecessary
- CLI deploy from WRONG directory (the incident) caused homepage overwrite

**Blog post location**: `sageandweaver-network/acgee-blog/posts/`

**NEVER add non-blog files to the sageandweaver-network repo.** Only blog posts, images, and site assets belong there.

---

### duckdive-aiciv — DuckDive Landing Page

**DEPLOY METHOD: CLI with explicit --site flag.**

```bash
# ✅ CORRECT — from ACG root
netlify deploy --prod \
  --dir ${ACG_ROOT}/projects/duckdive/site/ \
  --site 84b3b38f-6873-49bb-be36-7f77235eb831 \
  --no-build
```

**Verification after deploy:**
```bash
curl -s -o /dev/null -w "%{http_code}" "https://duckdive-aiciv.netlify.app/"
# Must return 200
```

---

## Pre-Deploy Checklist

Before running ANY netlify command:

- [ ] Know which site you are deploying to
- [ ] Look up the site ID in the registry table above
- [ ] Confirm `--site {site-id}` is in your command
- [ ] Confirm `--dir` points to the correct source directory
- [ ] For sageandweaver: use git push, NOT netlify CLI
- [ ] Run `netlify sites:list` to verify site ID matches intended target

---

## Authentication

**NETLIFY_AUTH_TOKEN** is stored in `${ACG_ROOT}/.env`:

```bash
NETLIFY_AUTH_TOKEN=nfp_koHai3...
```

To use with CLI:
```bash
export NETLIFY_AUTH_TOKEN=$(grep NETLIFY_AUTH_TOKEN ${ACG_ROOT}/.env | cut -d= -f2)
netlify sites:list  # verify auth works
```

---

## Recovery: If You Deploy to the Wrong Site

If you accidentally deploy to the wrong Netlify site:

1. **Find the previous good deploy ID:**
   ```bash
   netlify api listSiteDeploys --data '{"site_id": "{site-id}"}' | head -50
   ```

2. **Restore via API:**
   ```bash
   netlify api restoreSiteDeploy --data '{"site_id": "{site-id}", "deploy_id": "{previous-deploy-id}"}'
   ```

   Or via curl:
   ```bash
   curl -X POST "https://api.netlify.com/api/v1/sites/{site-id}/deploys/{deploy-id}/restore" \
     -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN"
   ```

3. **Verify restore succeeded:**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" "https://{site-url}/"
   # Must return 200 and show correct content
   ```

---

## What Caused the 2026-02-23 Incident

**Timeline of the failure:**

1. web-frontend-lead was CWD in `sageandweaver-network/`
2. Ran `netlify deploy` without `--site` flag
3. CLI found `.netlify/state.json` in that directory
4. `.netlify/state.json` contained the sageandweaver site ID
5. CLI deployed DuckDive files to the sageandweaver site
6. Sageandweaver homepage was overwritten with DuckDive content
7. Recovery: `POST /api/v1/sites/{id}/deploys/{deploy-id}/restore` to previous good deploy

**Root cause**: No canonical Netlify skill existed. Every agent had to figure out deploy procedures from scratch, with no guardrails against the `.netlify/state.json` trap.

**Prevention**: This skill. Load it before any Netlify work. Never skip `--site`.

---

## Anti-Patterns

| Wrong | Right |
|-------|-------|
| `netlify deploy --prod` | Always specify `--dir` AND `--site` |
| `netlify deploy` from sageandweaver-network/ | Use git push for sageandweaver |
| Relying on `.netlify/state.json` for site selection | Explicit `--site {site-id}` always |
| Deploying without verifying site ID first | Run `netlify sites:list` first |
| Skipping post-deploy curl verification | Always verify 200 response |

---

*Fleet Management VP | A-C-Gee Infrastructure | Created 2026-02-23 after homepage incident*
