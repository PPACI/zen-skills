# Vinted

Observed on vinted.fr, signed in through Claude in Chrome. Recheck routes and fields if a call fails.

Labels are quoted as the page shows them: English first, French in parentheses. The interface language is set in the header language menu (`FR` / `EN`); text returned by the API, such as order statuses, follows it.

## Pages

| Page | Path |
| --- | --- |
| Own profile, tabs "Active" / "Sold" ("Actifs" / "Vendus") | `/member/<user_id>`, from the avatar menu "My profile" ("Mon profil") |
| New listing | `/items/new` |
| Edit a listing | `/items/<id>/edit` |
| Inbox | `/inbox` |
| Notifications | `/member/notifications` |
| Orders | `/my_orders` |
| Wallet | `/wallet/balance` |

## Read-only API

Call from the signed-in page with `fetch(path, {headers: {accept: 'application/json'}})`.

| Data | Path | Useful fields |
| --- | --- | --- |
| Own listings | `/api/v2/wardrobe/<user_id>/items?page=1&per_page=20&order=relevance` | `id`, `title`, `price.amount`, `status` (condition), `is_closed` (sold), `is_reserved`, `is_hidden`, `is_draft`, `view_count`, `favourite_count`, `url`, `pagination.total_entries` |
| ISBN lookup | `/api/v2/item_upload/isbn_records?isbn=<isbn>` | title and author for that ISBN |
| One listing as edited | `/api/v2/item_upload/items/<id>` | `item.description`, `catalog_id`, `package_size_id`, `isbn`, `author`, `book_title`, `photos` |
| Conversations | `/api/v2/inbox?page=1&per_page=20` | `id`, `unread`, `description` (last message), `updated_at`, `opposite_user.login` |
| One conversation | `/api/v2/conversations/<id>` | `messages[]` (`entity_type`: `message`, `status_message`, `action_message` with shipping deadline), `transaction.status`, `allow_reply` |
| Sales | `/api/v2/my_orders?type=sold&status=all&page=1&per_page=20` | `title`, `price`, `status` ("Shipping label sent to seller." / "Bordereau envoyé au vendeur" = to ship), `date`, `conversation_id` |

`/api/v2/items/<id>/details` returns 403. `/api/v2/catalog/items` returns HTML, not JSON; search through the catalog page instead (see Market prices). Opening an unread conversation, through the page or the API, marks it read.

## Listing form

Fields appear as the category is chosen. The edit page has the same form.

1. "Photos": `input[type=file][name=photos]` (`data-testid="add-photos-input"`), multiple, JPEG/PNG/GIF/WebP. Fill it with the browser's file-upload tool, never by clicking (that opens a native picker).
2. "Title" ("Titre"), "Description".
3. "Category" ("Catégorie"): a drill-down menu, e.g. "Books & Media" › "Books" › "Fiction", "Non-fiction", "Kids & young adults", "Comics, manga & graphic novels", "Textbooks & study materials", "Colouring, puzzle & activity books" ("Livres et médias" › "Livres" › "Fiction", "Non-fiction", "Enfants et jeunes adultes", "Bandes dessinées, mangas et romans graphiques", "Manuels scolaires et ressources pédagogiques").
4. Category fields. Books: "ISBN", required to publish ("Please enter an ISBN to continue"); it fills "Author", "Book title", "Language". `GET /api/v2/item_upload/isbn_records?isbn=<isbn>` checks an ISBN and returns its record. Other categories were not checked.
5. "Condition" ("État"): "New with tags", "New without tags", "Very good", "Good", "Satisfactory" ("Neuf avec étiquette", "Neuf sans étiquette", "Très bon état", "Bon état", "Satisfaisant").
6. "Price" ("Prix") in euros. The buyer pays postage and a buyer-protection fee on top.
7. "Shipping" ("Envoi"), parcel size: "Small" (large envelope), "Medium" (shoebox), "Large" (moving box) ("Petit", "Moyen", "Grand"). One is marked "Recommended" ("Recommandé").
8. Buttons: new listing "Save draft" / "Upload" ("Sauvegarder le brouillon" / "Ajouter"); edit page "Save". Each needs the user's approval.

Leaving the form after touching any field raises a "Leave site?" dialog.

### Filling the form

Refs change on every page load: find each field again rather than reusing refs.

1. Photos: the browser's file-upload tool on the photos input; several files in one call work. On the edit page, each photo has a "Remove selected photo" button; remove from the last photo backwards.
2. "Title" and "Description": click, then type. To replace existing text, triple-click the title; click the description and select all (cmd+a) before typing.
3. "Category": open the picker, click each group button ("Books & Media", "Books"), then the leaf radio ("Non-fiction").
4. Books: type the ISBN, press Tab; author, book title, and language fill in. Check the language.
5. "Condition": open the picker, click the radio.
6. "Price": type, press Tab.
7. "Shipping": Vinted may preselect "Large" for a listing with several photos; set the size that fits.
8. Check the values before submitting: inputs `title`, `description`, `category`, `isbn`, `author`, `book_title`, `language_book`, `condition`, `price`, and `input:checked` for the parcel. The `bump` checkbox carries `value=1` but stays unchecked.
9. Click "Upload" (new) or "Save" (edit). Vinted redirects to the profile, after a new listing with an "Item listed" dialog. Confirm with `/api/v2/wardrobe/<user_id>/items?order=newest_first`.

## Price signals on the edit page

- "Price recommendation" shows three prices: "Bargain", "Optimal", "Premium". Computed by `POST https://api.vinted.fr/upload-form-suggestions/item_price_suggestions`.
- "See what similar items are selling for" opens "Similar sold items" with title, condition, and price (`POST …/upload-form-suggestions/item_upload/items/similar_sold_items`).
- Both are matched on the first book's ISBN and title, so they ignore that a listing is a lot. Use them as a floor for one book, not as the lot price.
- "Extras" offers a paid "Bump"; never select it without being asked.

## Seller workflow signals

- Offers arrive as conversation messages naming a price (French: "accepterais-tu de me vendre ceci à <price> ?") and are accepted or declined in the conversation.
- After a sale, the conversation shows a ship-by deadline ("Article à emballer et envoyer (avant le <date>)").
- The profile page shows views, favourites, and price per listing, and promotes paid "Showcase" and "Bump" ("Vitrine", "Booste tes articles"); never buy one without being asked.
