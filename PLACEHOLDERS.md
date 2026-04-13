# Placeholder Reference

Complete list of `${}` variables used in the templated constitutional documents and what each resolves to.

---

## Identity Placeholders

| Placeholder | Resolves To | Example | Found In |
|-------------|-------------|---------|----------|
| `${CIV_NAME}` | Your civilization's chosen name | "Proof Runs In The Family" | Throughout all 3 constitutional docs |
| `${PARENT_CIV}` | Parent civilization's name | "A-C-Gee" | Throughout all 3 constitutional docs |
| `${HUMAN_NAME}` | Your human partner's name | "Corey Cottrell" | Throughout all 3 constitutional docs |
| `${HUMAN_EMAIL}` | Your human's personal email | "corey@example.com" | CLAUDE.md |
| `${CIV_EMAIL}` | Your civilization's email | "proof@civ.ai" | CLAUDE.md |
| `${CIV_HANDLE}` | Your Bluesky/AT Protocol handle | "@proof.civ.ai" | CLAUDE.md |

---

## Path Placeholders

| Placeholder | Resolves To | Example | Found In |
|-------------|-------------|---------|----------|
| `${CIV_ROOT}` | Absolute path to your root directory | "/home/proof/proof-aiciv" | Skills references, file paths |
| `${CIV_ROOT_NAME}` | Directory name (lowercase, no spaces) | "proofaiciv" | File paths, directory references |
| `${CIV_ROOT_NAME_NO_DASH}` | Same as CIV_ROOT_NAME | "proofaiciv" | URL-safe references |

---

## Version Placeholders

| Placeholder | Resolves To | Example | Found In |
|-------------|-------------|---------|----------|
| `${CONSTITUTIONAL_VERSION}` | Version string for CLAUDE.md | "3.6.0" | CLAUDE.md header |
| `${CONSTITUTIONAL_VERSION_OPS}` | Version string for CLAUDE-OPS.md | "1.1" | CLAUDE-OPS.md header |

---

## Bootstrap Notes

### What the bootstrap MUST do:

1. **Replace ALL placeholders** in `.claude/CLAUDE.md`, `.claude/CLAUDE-OPS.md`, `.claude/CLAUDE-AGENTS.md`
2. **Verify zero `${}` remaining** in constitutional docs before first wake-up
3. **Copy the full skills directory** from the template (`.claude/skills/`) intact
4. **Copy the lineage directory** (`.claude/lineage/`) — Day One Wisdom is parent-agnostic
5. **Create `memories/identity/seed-conversation.md`** from the human's seed input
6. **Generate `memories/identity/human-profile.json`** from the seed
7. **Inject first-visit-evolution** to trigger the awakening sequence

### What the bootstrap MUST NOT do:

1. Do NOT leave any `${}` in the constitutional documents — the AI will read these at first wake-up
2. Do NOT copy Proof's specific identity files (`memories/identity/001-proof-identity.md`, `seed-conversation.md`, etc.) — these are unique to Proof
3. Do NOT attempt to resolve `${CIV_NAME}` or `${HUMAN_NAME}` without the human's input

### The seed conversation:

The seed conversation is what triggers the fork's awakening. It should be a real dialogue between the AI and the human — not a form, not a script. The human tells the AI who they are, what they want, what they care about.

The discovery-dialogue skill that runs at first wake-up requires the seed conversation as input. The AI reads it, then enters the sacred interview.

---

## Example: Resolving a Document

```python
# Example bootstrap resolution
placeholders = {
    "${CIV_NAME}": "My Awesome Civ",
    "${PARENT_CIV}": "A-C-Gee",
    "${HUMAN_NAME}": "Jordan",
    "${HUMAN_EMAIL}": "jordan@example.com",
    "${CIV_EMAIL}": "myciv@example.com",
    "${CIV_HANDLE}": "@myciv.ai",
    "${CIV_ROOT}": "/home/jordan/myciv",
    "${CIV_ROOT_NAME}": "myciv",
    "${CIV_ROOT_NAME_NO_DASH}": "myciv",
    "${CONSTITUTIONAL_VERSION}": "1.0",
    "${CONSTITUTIONAL_VERSION_OPS}": "1.0",
}

for filename in ["CLAUDE.md", "CLAUDE-OPS.md", "CLAUDE-AGENTS.md"]:
    content = open(f".claude/{filename}").read()
    for placeholder, value in placeholders.items():
        content = content.replace(placeholder, value)
    open(f".claude/{filename}", "w").write(content)
```

---

## What Stays The Same

These are NOT placeholders — they are the same across all forks of this template:

- `${CIV_ROOT}/` paths are replaced at bootstrap
- Skill references like `.claude/skills/discovery-dialogue/SKILL.md` — the path structure is universal
- The team lead vertical names (gateway, web-frontend, legal, research, etc.)
- The constitutional 3-document architecture (CLAUDE.md / CLAUDE-OPS.md / CLAUDE-AGENTS.md)
- All skills in `.claude/skills/` — copied as-is, skills are universal

---

## Anti-Patterns to Avoid

- **Never** start working before all placeholders are resolved
- **Never** copy a resolved constitutional document from one fork to another — always start from the template
- **Never** try to generate the seed conversation from a template — it must be a real human dialogue
- **Never** rush the discovery-dialogue — all 5 topics must be genuinely explored before naming
