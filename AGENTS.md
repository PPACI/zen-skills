# Zen skills repository rules

Skills and rules fail silently: no test catches one that became vague or self-contradictory. Read the whole file and its references before editing.

## Layout

- `templates/AGENTS.md`: modular global rules (4 independent `##` sections). Keep each bullet compact and token-efficient.
- `plugins/zen-<domain>/`: optional domain add-on plugins loaded on demand.

## Skill format

Every `plugins/<plugin>/skills/<name>/SKILL.md` starts with YAML frontmatter containing exactly two fields:

```yaml
---
name: skill-name
description: Use when [specific triggering condition]. [What it does.]
---
```

- `name`: a short phrase saying what the skill does (`make-images`), matching the folder. No `zen-` prefix: the plugin namespaces it.
- `description`: starts with "Use when", at most 1024 characters, states when to load the skill rather than summarizing its workflow.
- Move long material to `references/` inside the skill folder.

## Content

- Write templates, skills, and references in English, whatever language the conversation uses. Quote a site's interface text verbatim in its own language so it matches the page.
- Keep a rule only if it changes agent behavior away from its default and traces to a user preference, correction, or observed problem. Delete rules the harness already follows and rules already covered elsewhere.
- Skills are flat peers with no hub.
- Third-party skills worth using are vendored here and adapted, never installed as a dependency.
- Machine-, account-, or project-specific facts belong in `~/.agent-knowledge/` or the project, not in this public repository.
- Skills grow from the user's real tasks, but never mention the user's items, accounts, numbers, or dates. State each lesson generically: "one live description named the wrong volume", not which book.

## Packaging

- The repository root is the marketplace: `.claude-plugin/marketplace.json` (Claude Code) and `.agents/plugins/marketplace.json` (Codex) list every plugin in `plugins/`.
- Each plugin has one manifest, `plugins/<plugin>/plugin.json` (Agent Plugins 1.0). Keep `name` identical in all three manifests, and `description` identical in `plugin.json` and `.claude-plugin/marketplace.json`.
- Adding a plugin means a folder in `plugins/`, an entry in both marketplace files, and a row in the README.
- Do not add a `version`: without one, installs follow the latest commit.

## Check

```bash
claude plugin validate .claude-plugin/marketplace.json   # if Claude Code is installed
for p in plugins/*; do agy plugin validate "$p"; done    # or: claude plugin validate "$p"
jq -e '.plugins | map(.name)' .agents/plugins/marketplace.json >/dev/null
npx skills add . -l
```
