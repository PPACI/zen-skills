# Repricing listings that do not sell

Marketplace routes are in [vinted.md](vinted.md). Rules that depend on the kind of item are in [items/](items/).

## 1. Collect the listings

- Read active listings with price, condition, views, and favourites from the site's API.
- Listing age: Vinted's wardrobe API has no creation date; the first photo's `high_resolution.timestamp` is a usable proxy.
- For lots, read the description to get every item inside.
- Identify each item from the listing's photos before searching, not from the description or a code: descriptions can be wrong, and a guess from a barcode or ISBN prefix can be wrong.

## 2. Check the market

- Search each item separately, not the lot title: buyers search for one item. The item-type page says which terms to search.
- Run searches one at a time in the visible tab, about 5 seconds apart. About 30 parallel requests got the account "You are rate limited" for a few minutes.
- Vinted renders results in the browser: fetching the catalog page in the background returns no items, and `/api/v2/catalog/items` returns HTML. Navigate, wait about 5 seconds, then read the result cards' title and price from `main`'s text.
- Note the price range of comparable items in similar condition. Results mix in unrelated items; skip those.
- Vinted's own "Price recommendation" on the edit page matches only the first item of a lot. Do not use it for lot prices.

## 3. Read the signals

| Signal | Likely cause | Action |
| --- | --- | --- |
| Price already at or below the market range | Price is not the problem | Do not cut further; work on title, photos, or lot split |
| Few views | Buyers cannot find it: the title lacks the terms buyers search, or the lot mixes unrelated items | Put the searchable terms in the title; split mixed lots |
| Several favourites, no sale | Slightly high price, or buyers want one item of the lot | Small cut, or split |
| One item alone sells for more than the whole lot | The lot hides its value | Sell that item alone |

## 4. Propose

Present one table for approval: listing, current price, views and favourites, market range, proposal (new price, split, or new title), and the reason. Say which market prices were not checked.

## 5. Apply

Change only what the user approved, one listing at a time, saying each change in the chat before making it.

On Vinted, for each listing:

1. Open `/items/<id>/edit` and wait about 3 seconds.
2. Triple-click "Price" (or "Title"), type the new value, press Tab.
3. Check the form values before saving: `input[name=price]` reads the new price, `input[name=title]` holds the new title.
4. Click "Save". Vinted redirects to the profile.
5. Wait about 5 seconds (a fetch during the redirect fails), then confirm with `/api/v2/item_upload/items/<id>`.

After all changes, list the wardrobe once to confirm every price and title. A listing whose title changed shows `is_processing: true` for a while.

## 6. Split a lot

1. Get the lot's photos from `photos[].full_size_url` in `/api/v2/item_upload/items/<id>` and download them into a temporary folder (`original/<lot>/<n>.jpg`).
2. Look at each photo. Lot photos are often already one per item; crop only a photo that shows several items.
3. Copy the photos into one folder per future listing (`split/<nn>-<title>/<n>.jpg`), leaving the downloads untouched.
4. Present the new listings (title, price, photo folder) for approval.
5. Edit the lot into one of the items, keeping its favourites and history, then create new listings for the others, uploading photos with the browser's file-upload tool.
