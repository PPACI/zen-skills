# UI slop audit rubric

"Slop" is a style signal, not proof of AI authorship. Familiar fonts, colors, and components are not defects by themselves; question them when they compete with the user's task or say nothing.

## Patterns to question

| Area | Pattern |
| --- | --- |
| Type | Default-font convergence (Inter everywhere); all-caps labels |
| Color | Purple/lavender palettes; permanent dark mode; gradients and glows |
| Layout | Generic centered hero; identical icon-card grids; numbered steps; stat-tile rows; emoji sidebars |
| Decoration | Badges above headings; colored card borders or accent rails; glassmorphism; untouched component-library defaults |
| Copy | Slogans, reassurance, tutorials restating the controls, persistent "AI connected" or model badges |

## Keep, even when minimizing

Labels and units, accessible names, visible focus, error recovery, destructive-action consequences, material uncertainty, data-sharing disclosures, confirmations.

## Thresholds

- Normal text contrast at least 4.5:1; large text at least 3:1 (WCAG 2.2 SC 1.4.3).

## Sources

- Adrian Krebs, design slop patterns: https://www.adriankrebs.ch/blog/design-slop/
- Developers Digest, spotting AI design slop: https://www.developersdigest.tech/blog/ai-design-slop-and-how-to-spot-it
- NN/g, aesthetic and minimalist design: https://www.nngroup.com/articles/aesthetic-minimalist-design/
- NN/g, progressive disclosure: https://www.nngroup.com/articles/progressive-disclosure/
- WCAG 2.2 contrast minimum: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
