# Zen skills repository rules

Skills fail silently: no test catches a skill that became vague or self-contradictory. Read the whole `SKILL.md` and its references before editing it.

## Format

Every `skills/<name>/SKILL.md` starts with YAML frontmatter containing exactly two fields:

```yaml
---
name: zen-skill-name
description: Use when [specific triggering condition]. [What it does.]
---
```

- `name`: `zen-` plus a short phrase saying what the skill does (`zen-keep-it-simple`), matching the folder.
- `description`: starts with "Use when" (or "Use at" for always-on skills), at most 1024 characters, states when to load the skill rather than summarizing its workflow.
- Move long material to `references/` inside the skill folder.

## Content

- Keep a rule only if it changes agent behavior away from its default and traces to a user preference, correction, or observed problem. Delete rules the harness already follows and rules another skill already states.
- Skills are flat peers with no hub. Only the always-on skills are named in the bootloader in `README.md`; changing that set means editing every global file that holds it.
- Third-party skills worth using are vendored here and adapted, never installed as a dependency.
- Machine-, account-, or project-specific facts belong in `~/.agent-knowledge/` or the project, not in this public repository.

## Check

```bash
npx skills add . -l
```

Lists every skill the installer can parse.
