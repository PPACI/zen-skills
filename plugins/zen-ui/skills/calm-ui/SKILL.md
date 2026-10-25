---
name: calm-ui
description: Use when designing, building, reviewing, or checking a user interface, screen, page, or product copy. Removes decorative AI-style clutter, keeps what the user needs, and verifies the result across widths and states.
---

# Calm UI

Design around the user's task. Trust people with familiar controls. Guide with layout, hierarchy, spacing, and interaction before adding words.

## Design

- **Text earns its place.** Direct labels and actions. No slogans, reassurance, decorative eyebrows, repeated headings, or instructions that restate the controls. No default subtitle, helper sentence, empty-state paragraph, or tutorial.
- **AI information stays contextual.** No permanent assistant badges, model or reasoning pills, sparkles, or provider jargon. Show a failure beside the affected action; show truthful progress with cancellation; collapse finished activity. Diagnostics go behind Settings.
- **Content decides the layout.** No default hero, matching card grid, numbered steps, stat tiles, or explanatory sidebar. No decorative icons, empty charts, gradients, glows, or badges that say nothing. Familiar fonts and components are fine.
- **Minimal is not cryptic.** Keep labels, units, accessible names, focus states, error recovery, destructive-action consequences, material uncertainty, and data-sharing information. Text contrast at least WCAG AA. Reveal optional detail on demand.
- Parallel columns keep key controls top-aligned. No control floating alone in empty space; no overlapping text, chips, or panels.
- Never show users a checklist of these rules.

## Product language

- Labels, translation keys, errors, and progress messages name the user's task, never the SDK, model, infrastructure, or vendor.
- Refer to an AI vendor generically ("the app's AI provider"); show the service name only in Settings.
- Operator instructions (restart the server, configure keys) belong in docs or logs, never in product screens.

## New visual direction

Show several clearly different concepts side by side early (phone-size mockups) and let the user pick. Then follow the chosen direction exactly.

## Verify before reporting done

- Widths 320, 390, 768, 1280, 1440 px, with no horizontal page scroll.
- States: empty, populated, loading, result, error, dialogs; keyboard focus order and visible focus.
- Screenshots of affected states as evidence. Use disposable data; say when a response was faked.
- Name what a browser cannot prove when the change touches it: installed PWA, native build, device hardware, physical phone.
- Stop dev servers you started.

Audit rubric and sources: [references/audit-rubric.md](references/audit-rubric.md).
