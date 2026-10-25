---
name: cut-the-fluff
description: Use when writing or editing a README, documentation, code comment, docstring, article, post, email, AGENTS.md, CLAUDE.md, or SKILL.md. Keeps text compact, current, and free of AI writing patterns.
---

# Cut the fluff

## Documentation

- Keep only what a reader needs to use, operate, or safely change what exists now.
- READMEs: purpose, setup and run commands, required configuration, important limits, relevant checks. Link one source of detail instead of repeating it.
- Setup docs keep the bootstrap order, required tools, and where keys or secrets go (never their values).
- Git holds history: no change diaries, migration stories, abandoned approaches, completion reports, or lists of things not built.
- Describe the system as it ships, in the present tense: no "Phase 1", "MVP", "future", "now includes", "currently", unless the timing matters operationally.
- When behavior changes, edit and compact the existing text instead of appending.

## Comments

Explain a non-obvious invariant, reason, or hazard. Do not narrate code or describe hypothetical extensions. Keep comments that prevent data loss, security regressions, or wrong calculations.

## Prose for people

Before finalizing text that people will read, check it against [references/ai-writing-patterns.md](references/ai-writing-patterns.md).

## Agent instructions

- One source of truth in `AGENTS.md`; `CLAUDE.md` holds `@AGENTS.md` plus Claude-only notes.
- Write enduring rules, not plans. Include the check command to run before concluding.
- Do not repeat rules that the personal zen skills already cover.
- When the user agrees a new rule, update the file in the same change; keep stated non-negotiables unless the user changes them.
- Skills: `name` matches the folder; `description` states when to load it. Move long material to `references/`.
- Where each agent looks for these files: [references/agent-config.md](references/agent-config.md).
