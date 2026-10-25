---
name: sell-it
description: Use when preparing, pricing, publishing, or tracking items for sale on a second-hand marketplace such as Vinted or Leboncoin, including inventories of books or other objects from photos, checking listings, sales, and buyer messages, or driving the marketplace in a browser.
---

# Sell it

## Each listing

- Concise title, natural description, category, and the fields of the item's type.
- Condition only from the photos or the user's statement.
- Proposed price, with a short justification when asked.
- Path to the item's photo.
- Write in the marketplace's language.

## Accuracy

- Compare identifying details (title, brand, model, volume, size) against the photo before validating.
- When something is unreadable, mark it uncertain or ask for another photo. Never invent condition, brand, size, edition, code, or content.

## Item types

Rules that depend on the kind of item live in one page per type:

- Books, comics, manga: [references/items/books.md](references/items/books.md).

For a type with no page yet (clothes, electronics, …), apply only the general rules, and create `references/items/<type>.md` during the first job with that type, recording what that job taught: fields, search terms, pricing signals.

## Tracking

- Give each item a stable reference number (`001`, `002`, …). Never renumber without being asked.
- Keep one active tracker as the source of truth (an HTML page by default) with statuses such as For sale, Sold to ship, Shipped. Archived trackers stay read-only.
- Use relative paths so the folder stays portable; check every local link and thumbnail resolves after changes.
- Never modify or delete original photos.

## Browser

Pick the browser and sign in following [references/browsers.md](references/browsers.md). Marketplace pages, API routes, and form fields: [references/vinted.md](references/vinted.md). Listings that do not sell: [references/repricing.md](references/repricing.md).

## Publishing and replies

- Present listings (prices, condition, lots) for validation before publishing. Do not publish, save a draft, edit, or delete a live listing without explicit instruction.
- Draft replies to buyers and offers for the user to approve; send only the approved text.
- Report sales waiting to be shipped, with their deadline, whenever you check the account.
