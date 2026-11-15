# Leboncoin

Observed on leboncoin.fr through Claude in Chrome, account already signed in. Interface text is quoted in French as the page shows it. Recheck if a step changes.

## Pages

| Page | Path |
| --- | --- |
| New listing | `/deposer-une-annonce` |
| Boost options (after the form) | `/deposer-une-annonce/options` |
| Confirmation | `/deposer-une-annonce/confirmation` |
| Own listings, tabs "En ligne" / "Expirées" | `/compte/part/mes-annonces` |
| One listing | `/ad/<category>/<id>` |

## Listing form

1. "Quel est le titre de l'annonce ?": type the title. Suggested categories appear below it ("Maison & Jardin > Ameublement"); click one, or pick from "Ou choisissez une autre catégorie".
2. Photos (up to 20): fill the hidden file input ("Upload files") with the browser's file-upload tool, several files in one call, in display order; the first becomes "Couverture". Claude in Chrome uploads only files inside folders the session may read: copy them into the working folder first if they live elsewhere.
3. Category fields, prefilled from the title and photos: check each one. Furniture: "Type", "Produit", "Démontable" toggle, "Pièce", "Poids", "Marque", "Matière", "Couleur", "État" ("État neuf", "Très bon état", "Bon état", "État satisfaisant", "Pour pièces"). Electronics and appliances: "Type", "Produit", "Marque", "Poids", "Couleur", "Année de fabrication", "État". "Poids" drops the decimal point ("2.8" became "8"): type a whole number of kilograms. "Continuer".
4. "Un dernier aperçu avant de publier votre annonce !": Leboncoin writes its own description ("Rédigé par IA"). Replace it with the approved text.
5. "Prix de vente souhaité": shows "Prix recommandé entre X € et Y €" and a prefilled guess; set the approved price.
6. "Remise du bien" > "À quelle adresse se trouve le bien ?": type only the town and pick it from the list ("<Ville> (<code postal>)"); the street is not needed. "En main propre" is "Par défaut"; "Livraison personnalisée" shows "Désactivé" unless turned on. Some categories (pet accessories, appliances) instead show "En livraison" with "Activer la livraison" checked by default: uncheck it for a pickup-only item. With delivery on, Leboncoin guesses a parcel ("Colis moyen", "De 5 kg à 10 kg estimés"), which can be a size too heavy and makes postage dearer for the buyer. Its pencil button opens "Choisissez un format" ("Petit", "Moyen", "Volumineux"), then "Choisissez un poids" (classes from "Jusqu'à 100 g" to "Plus de 40 kg"); pick the class for the packed item and "Valider". For a free item, pick "Je donne" instead of "Je vends" under "Prix". "Continuer".
7. "Boostez votre annonce !": paid options, all unchecked. Never check one without being asked. "Déposer sans booster mon annonce" publishes.
8. A satisfaction survey may pop up on the confirmation page; close it without answering.

The listing appears under "Mes annonces" after moderation, usually about 30 seconds but sometimes several minutes; recheck later before reporting a problem. The public page lists "Modes de remise"; check it shows only "Remise en main propre" when the item is pickup only. The price line also shows a higher amount with "Transaction sécurisée incluse": the buyer's optional online-payment fee, not the seller's price.

## Starting the next listing

Wait for the confirmation page before opening `/deposer-une-annonce` again: Leboncoin keeps the form in progress per session, and a second form may overwrite it.
