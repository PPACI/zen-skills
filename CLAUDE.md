# Zen skills repository rules

Skills fail silently: no test catches a skill that became vague or self-contradictory. Read the whole `SKILL.md` and its references before editing it.

## Format

Every `plugins/<plugin>/skills/<name>/SKILL.md` starts with YAML frontmatter containing exactly two fields:

```yaml
---
name: skill-name
description: Use when [specific triggering condition]. [What it does.]
---
```

- `name`: a short phrase saying what the skill does (`keep-it-simple`), matching the folder. No `zen-` prefix: the `zen` plugin namespaces it (`zen:keep-it-simple` in Claude Code).
- `description`: starts with "Use when" (or "Use at" for always-on skills), at most 1024 characters, states when to load the skill rather than summarizing its workflow.
- Move long material to `references/` inside the skill folder.

## Content

- Keep a rule only if it changes agent behavior away from its default and traces to a user preference, correction, or observed problem. Delete rules the harness already follows and rules another skill already states.
- Skills are flat peers with no hub. Only the always-on skills are named in the bootloader in `README.md`; changing that set means editing every global file that holds it.
- Third-party skills worth using are vendored here and adapted, never installed as a dependency.
- Machine-, account-, or project-specific facts belong in `~/.agent-knowledge/` or the project, not in this public repository.

## Packaging

- The repository root is the marketplace: `.claude-plugin/marketplace.json` (Claude Code) and `.agents/plugins/marketplace.json` (Codex) list every plugin in `plugins/`.
- Each plugin has one manifest, `plugins/<plugin>/plugin.json` (Agent Plugins 1.0). Claude Code takes the plugin name and description from its marketplace entry, so keep `name` and `description` identical in all three places.
- `zen` is the core every machine installs: keep it to skills useful on any machine, including at work. Domain skills go in a `zen-<domain>` add-on.
- Adding a plugin means a folder in `plugins/`, an entry in both marketplace files, and a row in the README.
- Do not add a `version`: without one, installs follow the latest commit.

## Check

```bash
claude plugin validate .claude-plugin/marketplace.json
for p in plugins/*; do claude plugin validate "$p"; done
npx skills add . -l
```
