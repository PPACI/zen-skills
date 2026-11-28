# zen-skills

**Calm, opinionated `AGENTS.md` rules and domain [Agent Skills](https://agentskills.io) for Antigravity, Claude Code, and Codex.**

Core behavior lives as a compact, modular `AGENTS.md` template (zero startup tool calls, ~560 tokens total) that you copy in full or section by section. Task-specific workflows live as optional add-on plugins that load only when needed.

```text
zen-skills
│
├── templates/AGENTS.md     paste in full or pick the sections you want
│   ├── Communication           answer first, scannable, ranked options, batched questions
│   ├── Memory                  shared local agent memory (~/.agent-knowledge/)
│   ├── Engineering & safety    proportional risk, YAGNI, one MR at a time, risk-based secrets
│   └── Writing & docs          present-tense docs, useful comments, lean agent files
│
└── plugins/                optional domain add-ons
    ├── zen-colab           run-colab-ollama  Ollama on Colab GPUs, exposed locally over SSH
    ├── zen-images          make-images       OpenRouter image generation that works
    └── zen-resale          sell-it           Vinted / Leboncoin listings from photos
                            print-labels      shipping labels on Avery L7169 sheets
```

## Quick start

### 1. Global rules (`AGENTS.md`)

Copy [templates/AGENTS.md](templates/AGENTS.md) (in full, or pick only the `##` sections you want) into your global agent instructions file:

| Harness | Global file |
| --- | --- |
| Antigravity | `~/.gemini/config/AGENTS.md` |
| Claude Code | `~/.claude/CLAUDE.md` |
| Codex | `~/.codex/AGENTS.md` |

| Section | What it changes |
| --- | --- |
| **Communication** | Answer or command first, tables and short grouped lists over paragraphs, ranked options with tradeoffs, brief progress with proof, batched questions. |
| **Memory** | Agent reads and maintains `~/.agent-knowledge/`, a local folder of linked Markdown notes shared across harnesses. |
| **Engineering & safety** | Risk-proportional checks and secret handling, smallest clear change, one MR/PR at a time, stdlib first, no unrequested commits. |
| **Writing & docs** | Present-tense docs without change diaries, comments for invariants/hazards only, natural prose without AI clichés, single `AGENTS.md` source of truth. |

### 2. Optional domain plugins

Install only the add-ons you need:

- **Antigravity**: clone this repo and symlink plugins into `~/.gemini/config/plugins/`:

  ```bash
  git clone https://github.com/PPACI/zen-skills.git ~/Code/zen-skills
  mkdir -p ~/.gemini/config/plugins
  ln -sfn ~/Code/zen-skills/plugins/zen-images ~/.gemini/config/plugins/zen-images
  ```

- **Claude Code**:

  ```bash
  claude plugin marketplace add PPACI/zen-skills
  claude plugin install zen-images@zen-skills
  ```

- **Codex**:

  ```bash
  codex plugin marketplace add PPACI/zen-skills
  codex plugin add zen-images@zen-skills
  ```

- **Other agents**: install skills directly without the plugin system:

  ```bash
  npx skills add PPACI/zen-skills -g
  ```

**Updates.** Plugins have no pinned version, so updates follow the latest commit (`git pull` for symlinked Antigravity plugins, `claude plugin marketplace update zen-skills` or auto-update for Claude Code, `codex plugin marketplace upgrade zen-skills` for Codex).

## Domain skills

| Plugin | Skill | Loads when | What changes |
| --- | --- | --- | --- |
| zen-colab | [run-colab-ollama](plugins/zen-colab/skills/run-colab-ollama/SKILL.md) | Ollama on Google Colab | Checks/bootstraps `google-colab-cli` and SSH `ProxyCommand`, sizes GPU (`T4`/`L4`/`A100`) to model VRAM to save compute units, runs Ollama with `q8_0` KV cache over SSH, exposes a local OpenAI-compatible port, and guards against idle VM billing. |
| zen-images | [make-images](plugins/zen-images/skills/make-images/SKILL.md) | OpenRouter image work | Endpoint per model family, HTTP 400 pitfalls, observed costs, recipes for realistic portraits, faithful product cleanup, cartoons, sticker packs, and SVG output. |
| zen-resale | [sell-it](plugins/zen-resale/skills/sell-it/SKILL.md) | Second-hand listings | Listing fields, no invented condition or ISBN, faithful AI-cleaned photos, Leboncoin pickup for bulky items, stable references, one tracker, nothing published without approval. |
| zen-resale | [print-labels](plugins/zen-resale/skills/print-labels/SKILL.md) | Shipping labels to print | Crops the carrier label out of the PDF or image and places it on a blank A4 landscape page at the chosen Avery L7169 position, barcodes kept vector. |

## How it fits with work instructions

```text
chat  >  project / work AGENTS.md  >  zen rules
```

Paste the sections you want at the end of your work `AGENTS.md` (with the precedence line at the top), and work rules win on any conflict.

## Packaging

| File | Read by |
| --- | --- |
| `templates/AGENTS.md` | Copied or symlinked into global agent instructions |
| `.claude-plugin/marketplace.json` | Claude Code |
| `.agents/plugins/marketplace.json` | Codex |
| `plugins/<name>/plugin.json` | Antigravity, Codex, and [Agent Plugins 1.0](https://agent-plugins.org) clients |
| `plugins/<name>/skills/` | Everyone |

## Checks

Authoring rules and validation commands live in [AGENTS.md](AGENTS.md).
