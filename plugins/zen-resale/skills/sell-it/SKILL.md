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

## Marketplace

- Vinted works only through parcel shipping. Bulky or heavy items (furniture, large appliances) go on Leboncoin with hand delivery ("Remise en main propre") instead.
- Say which marketplace you picked and why in one line.

## Accuracy

- Compare identifying details (title, brand, model, volume, size) against the photo before validating.
- When something is unreadable, mark it uncertain or ask for another photo. Never invent condition, brand, size, edition, code, or content.

## Photos

- Rotate phone photos to upright pixels before cropping or sending them anywhere: many exports keep the rotation only in an EXIF orientation tag that tools and image APIs ignore.
- Check every photo meant for publication for personal items in the frame: ID documents, letters, screens, addresses.
- AI-cleaned photos (clutter removed, plain background) are fine when the user wants them, but the item must stay faithful:
  - Compare each generated image with the real photos: same proportions, count of parts, colour, finish.
  - Before generating, ask for close-ups of the surfaces buyers will inspect (top, edges, corners) and pass them as extra references.
  - Keep real defects. Show each one in its own AI-cleaned close-up that keeps the defect, and name it in the description.
- Image generation itself: use `make-images` if installed.

## Item types

Rules that depend on the kind of item live in one page per type:

- Books, comics, manga: [references/items/books.md](references/items/books.md).
- Furniture: [references/items/furniture.md](references/items/furniture.md).
- Electronics and small appliances: [references/items/electronics.md](references/items/electronics.md).

For a type with no page yet (clothes, toys, …), apply the general rules.

## Tracking

For multi-item local batches (skip when listing 1–3 items or checking live listings):

- Give each item a stable reference number (`001`, `002`, …). Never renumber without being asked.
- Keep one tracker as the source of truth (Markdown or CSV by default; HTML only when visual thumbnails help) with statuses such as For sale, Sold to ship, Shipped.
- Use relative paths so the folder stays portable; check local links resolve after changes.
- Never modify or delete original photos.

## Browser

Pick the browser and sign in following [references/browsers.md](references/browsers.md). Marketplace pages, API routes, and form fields: [references/vinted.md](references/vinted.md), [references/leboncoin.md](references/leboncoin.md). Listings that do not sell: [references/repricing.md](references/repricing.md).

## Publishing and replies

- Present listings (prices, condition, lots) for validation before publishing. Do not publish, save a draft, edit, or delete a live listing without explicit instruction.
- Draft replies to buyers and offers for the user to approve; send only the approved text.
- Report sales waiting to be shipped, with their deadline, whenever you check the account.
