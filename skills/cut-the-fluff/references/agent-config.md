# Where agents read instructions and skills

Verified 2026-10-24 against official docs; this changes often, so recheck before relying on it.

| Location | Claude Code | Codex | Cursor | VS Code / Copilot |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | Only when no `CLAUDE.md` exists | Yes, merged root → cwd | Yes | Yes |
| `.claude/skills/` | Yes | No | Yes | Yes |
| `.agents/skills/` | No | Yes | Yes | Yes |

- Agent Skills spec (agentskills.io) requires only `name` and `description`, and defines no discovery path.
- `npx skills add <owner/repo> -g -a claude-code -a codex` installs to `~/.agents/skills/` and symlinks each skill into `~/.claude/skills/`.

## Plugins (verified 2026-10-25)

| | Claude Code | Codex |
| --- | --- | --- |
| Plugin manifest | `.claude-plugin/plugin.json` (optional; only `name` required) | Root `plugin.json` per Agent Plugins 1.0 (preferred); `.codex-plugin/plugin.json` as fallback |
| Skills | `skills/<name>/SKILL.md` | Same |
| Marketplace | `.claude-plugin/marketplace.json` | `.agents/plugins/marketplace.json`; also reads `.claude-plugin/marketplace.json` |
| Skill name once installed | `<plugin>:<skill>` | Not documented |
| Updates | Pinned by `version`; omit it to track commits. Third-party marketplace auto-update is off by default | `codex plugin marketplace upgrade` |

Agent Plugins 1.0 (agent-plugins.org) covers skills and MCP only; Claude Code does not document support for it.
