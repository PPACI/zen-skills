# zen-skills

**Calm, opinionated agent skills that make Claude Code and Codex answer first, build less, and write without fluff.**

A plugin marketplace with one core plugin and a few add-ons, all made of small [Agent Skills](https://agentskills.io). The core replaces a 15 KB global `CLAUDE.md` with a three-line bootloader. Each skill loads only when its task shows up, and your project or work instructions always win.

```text
zen-skills marketplace
│
├── zen                core, install everywhere
│   ├── zen:answer-first      always on   replies you can act on
│   ├── zen:remember-this     always on   a memory agents keep for themselves
│   ├── zen:keep-it-simple    code        YAGNI, small diffs, no surprise commits
│   └── zen:cut-the-fluff     writing     docs and prose without AI tells
│
├── zen-ui             add-on     calm-ui       no sparkles, no badges, checked at 320 px
├── zen-images         add-on     make-images   OpenRouter image generation that works
└── zen-resale         add-on     sell-it       Vinted / Leboncoin listings from photos
```

## Quick start

1. Add the marketplace and install the core.

   Claude Code:

   ```bash
   claude plugin marketplace add PPACI/zen-skills
   claude plugin install zen@zen-skills
   ```

   Codex: add the marketplace, then install **zen** from the plugin directory in the Codex app.

   ```bash
   codex plugin marketplace add PPACI/zen-skills
   ```

2. Paste the bootloader into `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, or your work `AGENTS.md`:

   ```markdown
   # Zen skills

   At the start of every session, load the `answer-first` and `remember-this` skills from the zen plugin (`zen:answer-first` and `zen:remember-this` in Claude Code). Load other zen skills when their description matches the task.
   Project and work instructions override zen skills when they conflict.
   ```

3. Add the add-ons you need, for example:

   ```bash
   claude plugin install zen-ui@zen-skills
   ```

**Updates.** Plugins have no pinned version, so each update follows the latest commit. Claude Code: turn on auto-update for the marketplace in `/plugin`, or run `claude plugin marketplace update zen-skills`. Codex: `codex plugin marketplace upgrade zen-skills`.

**Other agents.** The skills also install without the plugin system, for any agent that reads Agent Skills: `npx skills add PPACI/zen-skills -g`.

## The skills

| Plugin | Skill | Loads when | What changes |
| --- | --- | --- | --- |
| zen | [answer-first](plugins/zen/skills/answer-first/SKILL.md) | Every session | Answer or command first, tables and bullets over paragraphs, visible progress, one next step you can do in two minutes. Built for readers with ADHD; nice for everyone else. |
| zen | [remember-this](plugins/zen/skills/remember-this/SKILL.md) | Every session | The agent reads and maintains `~/.agent-knowledge/`, a local folder of linked Markdown notes shared by every harness. It never leaves your machine. |
| zen | [keep-it-simple](plugins/zen/skills/keep-it-simple/SKILL.md) | Code, config, infra, tests | Smallest change that works, standard library first, direct edits over wrapper scripts, tests in proportion to risk, test-first when the project asks, no commit you didn't request. |
| zen | [cut-the-fluff](plugins/zen/skills/cut-the-fluff/SKILL.md) | Docs, comments, prose, agent files | READMEs that only say what you need now, comments that explain hazards, prose checked against a catalogue of AI writing patterns, one `AGENTS.md` per repo. |
| zen-ui | [calm-ui](plugins/zen-ui/skills/calm-ui/SKILL.md) | Interfaces and product copy | No hero-and-card-grid defaults, no "AI connected" badges, vendor-neutral labels, several concepts before one polished one, then checks at five widths. |
| zen-images | [make-images](plugins/zen-images/skills/make-images/SKILL.md) | OpenRouter image work | Which endpoint each model family needs, parameters that return HTTP 400, observed costs, and a recipe for realistic portraits. |
| zen-resale | [sell-it](plugins/zen-resale/skills/sell-it/SKILL.md) | Second-hand listings | Listing fields, no invented condition or ISBN, stable references, one tracker, nothing published without your approval. |

## How it fits with work instructions

Global instruction files are hard to share between a personal setup and a company one: you end up merging two long files by hand. Here the personal part is three lines plus plugins:

```text
chat  >  project / work AGENTS.md  >  zen skills
```

Put the bootloader at the end of your work `AGENTS.md`, install only `zen`, and both sets of rules apply, with work rules winning on any conflict.

## How it's packaged

| File | Read by |
| --- | --- |
| `.claude-plugin/marketplace.json` | Claude Code |
| `.agents/plugins/marketplace.json` | Codex |
| `plugins/<name>/plugin.json` | Codex and other [Agent Plugins 1.0](https://agent-plugins.org) clients; Claude Code takes the name from the marketplace entry |
| `plugins/<name>/skills/` | Everyone |

## Make it yours

Fork the repo and edit the skills; they are plain Markdown. The repository rules in [CLAUDE.md](CLAUDE.md) keep them lean:

- A rule stays only if it changes the agent's default behavior and traces back to a real preference or a real mistake.
- Long reference material goes in a skill's `references/` folder, read only when needed.
- Third-party skills worth having get vendored and adapted here, not installed as dependencies.

Check the marketplace and each plugin still validate:

```bash
claude plugin validate .claude-plugin/marketplace.json
for p in plugins/*; do claude plugin validate "$p"; done
```
