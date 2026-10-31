---
name: print-labels
description: Use when the user gives a shipping label (Colissimo, Mondial Relais, Relais Colis, Chronopost, from Vinted, Leboncoin or elsewhere, as PDF or image) to print on a sheet of four Avery L7169 labels, or names a sheet position such as "top left" or "en haut à gauche". Crops the label and places it on a blank A4 landscape PDF.
---

# Print labels

`scripts/labels.py` (in this skill's folder) crops each shipping label and places it on a blank A4 landscape page laid out like an Avery L7169 sheet: four 139 × 99 mm labels, no template outlines. Run it with `uv run`; it installs PyMuPDF itself and keeps the label vector, so barcodes stay sharp.

## Positions

Positions are as seen with the sheet in landscape, the same way up as the user's reference template. Codes: `tl`, `tr`, `bl`, `br` (French `hg`, `hd`, `bg`, `bd` also work). Ask for the position when it is missing. Labels given together go on one sheet.

## Steps

1. Copy each source file into a new, empty scratch folder.
2. Inspect: `uv run <skill-dir>/scripts/labels.py inspect SOURCE --out SCRATCH`. It prints the page size, the non-white area and large rectangles (often the label frame), and writes a PNG with a millimetre grid. Read the PNG.
3. Pick the crop in mm from the page's top-left corner. Keep only what goes on the parcel: addresses, barcodes, QR code, routing codes, carrier marks such as "DEPOT PRIO". Leave out instructions, proof of postage, "Collez ici le ruban adhésif", cut lines and ads. Add about 0.5 mm around the frame.
4. Build:
   ```bash
   uv run <skill-dir>/scripts/labels.py build \
     --out labels-YYYY-MM-DD-HHMM.pdf \
     --place "tl:SOURCE:0:x0,y0,x1,y1" \
     --preview SCRATCH/preview.png
   ```
   `--place` is `POS:SOURCE[:PAGE[:CROP[:ROT]]]`, once per label. `ROT` defaults to `auto`: 90° when the crop is portrait.
5. Read the preview (grey outlines are the labels and are not in the PDF): everything inside the right box, nothing cut off.
6. If the printed scale is under 90 %, tighten the crop; shrunken barcodes may not scan. Say so if it cannot go higher.

Write the PDF to the current working directory unless the user names another folder. Remind the user to print at 100 % / actual size, not "fit to page".

## Carrier formats

- **Colissimo from Vinted**: A4 landscape page, label in the left half. Inner frame about 100 × 120 mm at `20,32,120,152`, with "DEPOT PRIO" below it. Crop `19.5,31.5,120.5,175`, rotated 90°, prints at 93 %.

Add a line here for each new format met.
