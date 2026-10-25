---
name: sell-it
description: Use when preparing, pricing, publishing, or tracking items for sale on a second-hand marketplace such as Vinted or Leboncoin, including inventories of books or other objects from photos.
---

# Sell it

## Each listing

- Concise title, natural description, category, language (for books), author or brand when verifiable.
- Condition only from the photos or the user's statement.
- Proposed price, with a short justification when asked.
- Path to the item's photo.
- Write in the marketplace's language.

## Accuracy

- Compare titles, volume numbers, and editions against the photo before validating.
- When something is unreadable, mark it uncertain or ask for another photo. Never invent condition, edition, ISBN, or content.

## Tracking

- Give each item a stable reference number (`001`, `002`, …). Never renumber without being asked.
- Keep one active tracker as the source of truth (an HTML page by default) with statuses such as For sale, Sold to ship, Shipped. Archived trackers stay read-only.
- Use relative paths so the folder stays portable; check every local link and thumbnail resolves after changes.
- Never modify or delete original photos.

## Publishing

Present listings (prices, condition, lots) for validation before publishing. Do not publish, edit, or delete a live listing without explicit instruction.
