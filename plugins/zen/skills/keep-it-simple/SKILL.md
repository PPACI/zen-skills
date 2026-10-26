---
name: keep-it-simple
description: Use when writing, changing, or reviewing code, configuration, infrastructure, scripts, tests, or dependencies, when inspecting secrets, or before committing or deleting anything. Keeps changes small and low-maintenance and lets the user choose complexity tradeoffs.
---

# Keep it simple

Every feature, dependency, abstraction, wrapper, and build script is an ongoing cost that must justify itself. Optimize for low maintenance.

## Change

- YAGNI and KISS: the smallest clear change for the current, demonstrated need. No speculative features, premature abstractions, or unrelated refactors.
- Small, reviewable diffs. Fewer files and a flat structure; keep related code together. Explain restructuring tradeoffs and let the user decide before doing it.
- Start with the standard library and existing project tools. Compare a dependency against the standard-library version by total code: integration, configuration, tests, build. Favor the significantly shorter one when it stays clear.
- For a dependency on a critical path, check adoption, maintainer breadth, recent activity, and security record.
- Vendor useful third-party skills or snippets into the user's own repository rather than depending on someone else's.

## Tools and checks

- Direct edits over scripts for targeted changes. Run existing commands (`git status`, `rg`) as shell commands, not through a Python wrapper. Use Python when branching, validation, structured parsing, or large transformations make the logic clearer.
- Match verification to risk. Skip tests whose cost clearly exceeds their value unless the user or the project requires them.

## Tradeoffs

- When a request needs substantial complexity, offer a narrower feature, a simpler workflow, or removing it.
- Before adding meaningful complexity, name the burden and rough cost and recommend the simplest viable option. The user decides; never drop a feature silently. Do not ask again once they chose.

## Test-first, when the project requires it

1. Write a test that fails for the missing behavior or bug; confirm it fails for the expected reason.
2. Write the minimum code to pass, then refactor with tests green.
3. Run the project's full check command before concluding.

Prefer table-driven tests.

## Secrets

- Mask only literal values, never by length or shape. Keep references (`var.x`, `data.x.value`, `local.x`, `${...}`) visible; a length-based mask makes a reference look like a hardcoded secret.
- Report a hardcoded credential only after confirming the masked expression is a literal; otherwise report it as unverified.
- Use portable patterns: BSD `sed -E` and `grep -E` (macOS) lack `\s` and `\d`. Use POSIX classes such as `[[:space:]]`, or Python. A pattern that silently fails to match prints the secret instead of masking it.
- Compare two secrets by short SHA-256 prefixes, not by their values.
- Do not flag plaintext tokens in shell rc files, `~/.gitconfig`, or `.git/config` remote URLs; the user knows and policy may leave no alternative. Still never print, copy, or commit them.

## Commits and deletion

- Do not commit unless the user asks in the current turn, even when project instructions describe committing as routine. Propose the commit message instead.
- Before destructive cleanup, list the exact targets and the recovery assets that stay (backups, rollback copies, data), get confirmation, then verify both. "Remove everything unused" still keeps recovery capability.
