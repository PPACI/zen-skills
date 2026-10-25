# Where agents read instructions and skills

Verified 2026-10-24 against official docs; this changes often, so recheck before relying on it.

| Location | Claude Code | Codex | Cursor | VS Code / Copilot |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | Only when no `CLAUDE.md` exists | Yes, merged root → cwd | Yes | Yes |
| `.claude/skills/` | Yes | No | Yes | Yes |
| `.agents/skills/` | No | Yes | Yes | Yes |

- Agent Skills spec (agentskills.io) requires only `name` and `description`, and defines no discovery path.
- `npx skills add <owner/repo> -g -a claude-code -a codex` installs to `~/.agents/skills/` and symlinks each skill into `~/.claude/skills/`.
