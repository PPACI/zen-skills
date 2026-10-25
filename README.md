# zen-skills

**Calm, opinionated agent skills that make Claude Code and Codex answer first, build less, and write without fluff.**

Seven small [Agent Skills](https://agentskills.io) that replace a 15 KB global `CLAUDE.md` with a three-line bootloader. Each skill loads only when its task shows up, and your project or work instructions always win.

```text
~/.claude/CLAUDE.md  (3 lines)
│
├── zen-answer-first      always on   replies you can act on
├── zen-remember-this     always on   a memory agents keep for themselves
│
├── zen-keep-it-simple    code        YAGNI, small diffs, no surprise commits
├── zen-cut-the-fluff     writing     docs and prose without AI tells
├── zen-calm-ui           UI          no sparkles, no badges, checked at 320 px
├── zen-make-images       images      OpenRouter image generation that works
└── zen-sell-it           resale      Vinted / Leboncoin listings from photos
```

## Quick start

1. Install every skill for Claude Code and Codex:

   ```bash
   npx skills add PPACI/zen-skills -g -a claude-code -a codex -s '*' -y
   ```

2. Paste the bootloader into `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, or your work `AGENTS.md`:

   ```markdown
   # Zen skills

   At the start of every session, load the `zen-answer-first` and `zen-remember-this` skills. Load other `zen-*` skills when their description matches the task.
   Project and work instructions override `zen-*` skills when they conflict.
   ```

3. Start a new session and ask anything. The answer comes first.

Update later with `npx skills update -g`.

## The skills

| Skill | Loads when | What changes |
| --- | --- | --- |
| [zen-answer-first](skills/zen-answer-first/SKILL.md) | Every session | Answer or command first, tables and bullets over paragraphs, visible progress, one next step you can do in two minutes. Built for readers with ADHD; nice for everyone else. |
| [zen-remember-this](skills/zen-remember-this/SKILL.md) | Every session | The agent reads and maintains `~/.agent-knowledge/`, a local Git repo of linked Markdown notes shared by every harness. It never leaves your machine. |
| [zen-keep-it-simple](skills/zen-keep-it-simple/SKILL.md) | Code, config, infra, tests | Smallest change that works, standard library first, direct edits over wrapper scripts, tests in proportion to risk, test-first when the project asks, no commit you didn't request. |
| [zen-cut-the-fluff](skills/zen-cut-the-fluff/SKILL.md) | Docs, comments, prose, agent files | READMEs that only say what you need now, comments that explain hazards, prose checked against a catalogue of AI writing patterns, one `AGENTS.md` per repo. |
| [zen-calm-ui](skills/zen-calm-ui/SKILL.md) | Interfaces and product copy | No hero-and-card-grid defaults, no "AI connected" badges, vendor-neutral labels, several concepts before one polished one, then checks at five widths. |
| [zen-make-images](skills/zen-make-images/SKILL.md) | OpenRouter image work | Which endpoint each model family needs, parameters that return HTTP 400, observed costs, and a recipe for realistic portraits. |
| [zen-sell-it](skills/zen-sell-it/SKILL.md) | Second-hand listings | Listing fields, no invented condition or ISBN, stable references, one tracker, nothing published without your approval. |

## How it fits with work instructions

Global instruction files are hard to share between a personal setup and a company one: you end up merging two long files by hand. Here the personal part is just three lines plus skills:

```text
chat  >  project / work AGENTS.md  >  zen-* skills
```

Put the bootloader at the end of your work `AGENTS.md` and both sets of rules apply, with work rules winning on any conflict.

## Make it yours

Fork the repo and edit the skills; they are plain Markdown. The repository rules in [CLAUDE.md](CLAUDE.md) keep them lean:

- A rule stays only if it changes the agent's default behavior and traces back to a real preference or a real mistake.
- Long reference material goes in a skill's `references/` folder, read only when needed.
- Third-party skills worth having get vendored and adapted here, not installed as dependencies.

Check that every skill still parses:

```bash
npx skills add . -l
```
