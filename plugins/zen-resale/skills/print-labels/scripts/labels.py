# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf>=1.24"]
# ///
"""Place shipping labels on an A4 landscape sheet of 4 Avery L7169 labels.

  uv run labels.py inspect SOURCE [--page N] [--out DIR]
  uv run labels.py build --out FILE.pdf --place POS:SOURCE[:PAGE[:CROP[:ROT]]] ...

POS: tl, tr, bl, br (top/bottom left/right), or French hg, hd, bg, bd.
CROP: x0,y0,x1,y1 in mm from the top-left of the source page, or "full".
ROT: 0, 90, 180, 270 or "auto" (default: rotate when it fits the label better).
"""
import argparse
import sys
from pathlib import Path

import pymupdf

MM = 72 / 25.4
A4_LANDSCAPE = pymupdf.Rect(0, 0, 297 * MM, 210 * MM)

# Label boxes in mm, measured on Avery's L7169 Word template exported as A4 landscape.
LABELS_MM = {
    "tl": (9.5, 4.8, 148.5, 103.8),
    "tr": (148.5, 4.8, 287.5, 103.8),
    "bl": (9.5, 106.4, 148.5, 205.5),
    "br": (148.5, 106.4, 287.5, 205.5),
}
ALIASES = {"hg": "tl", "hd": "tr", "bg": "bl", "bd": "br"}
INSET_MM = 2.5  # keep content off the label edges and die cut


def mm_rect(x0, y0, x1, y1):
    return pymupdf.Rect(x0 * MM, y0 * MM, x1 * MM, y1 * MM)


def load_page(source, pno=0):
    """Return a one-page PDF with rotation baked in, from a PDF or an image."""
    src = pymupdf.open(source)
    if not src.is_pdf:
        src = pymupdf.open("pdf", src.convert_to_pdf())
    page = src[pno]
    out = pymupdf.open()
    new = out.new_page(width=page.rect.width, height=page.rect.height)
    new.show_pdf_page(new.rect, src, pno)
    return out


def content_bbox(page, dpi=50):
    """Bounding box of non-white pixels, in points."""
    pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY, alpha=False)
    w, h, s = pix.width, pix.height, pix.samples
    rows = [y for y in range(h) if min(s[y * w:(y + 1) * w]) < 200]
    if not rows:
        return None
    cols = [x for x in range(w) if min(s[x::w][rows[0]:rows[-1] + 1]) < 200]
    k = 72 / dpi
    return pymupdf.Rect(cols[0] * k, rows[0] * k, (cols[-1] + 1) * k, (rows[-1] + 1) * k)


def fmt(r):
    return ",".join(f"{v / MM:.1f}" for v in (r.x0, r.y0, r.x1, r.y1))


def inspect(args):
    src = pymupdf.open(args.source)
    print(f"{args.source}: {len(src)} page(s)")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    pages = [args.page] if args.page is not None else range(len(src))
    for pno in pages:
        doc = load_page(args.source, pno)
        page = doc[0]
        r = page.rect
        print(f"\npage {pno}: {r.width / MM:.1f} x {r.height / MM:.1f} mm")
        bbox = content_bbox(page)
        print(f"  content bbox (mm): {fmt(bbox) if bbox else 'empty'}")
        boxes = []
        for d in page.get_drawings():
            dr = d["rect"]
            if dr.width > 40 * MM and dr.height > 40 * MM and dr != r:
                dash = " dashed" if d.get("dashes") not in (None, "[] 0") else ""
                boxes.append(f"  rect{dash} (mm): {fmt(dr)}")
        print("\n".join(dict.fromkeys(boxes)) or "  no large rectangles")
        # Grid every 10 mm, labelled every 50 mm, to read crop coordinates.
        shape = page.new_shape()
        for x in range(0, int(r.width / MM) + 1, 10):
            shape.draw_line((x * MM, 0), (x * MM, r.height))
            shape.finish(color=(1, 0, 0) if x % 50 == 0 else (1, 0.75, 0.75), width=0.4)
            if x % 50 == 0:
                page.insert_text((x * MM + 2, 10), str(x), fontsize=8, color=(1, 0, 0))
        for y in range(0, int(r.height / MM) + 1, 10):
            shape.draw_line((0, y * MM), (r.width, y * MM))
            shape.finish(color=(0, 0, 1) if y % 50 == 0 else (0.75, 0.75, 1), width=0.4)
            if y % 50 == 0:
                page.insert_text((2, y * MM - 2), str(y), fontsize=8, color=(0, 0, 1))
        shape.commit()
        png = out_dir / f"{Path(args.source).stem}.p{pno}.grid.png"
        page.get_pixmap(dpi=110).save(png)
        print(f"  grid preview: {png}")


def parse_place(spec):
    parts = spec.split(":")
    pos = ALIASES.get(parts[0].lower(), parts[0].lower())
    if pos not in LABELS_MM:
        sys.exit(f"unknown position {parts[0]!r}; use tl, tr, bl, br")
    source, rest = parts[1], parts[2:]
    pno = int(rest[0]) if len(rest) > 0 and rest[0] else 0
    crop = rest[1] if len(rest) > 1 and rest[1] else "full"
    rot = rest[2] if len(rest) > 2 and rest[2] else "auto"
    return pos, source, pno, crop, rot


def build(args):
    out = pymupdf.open()
    sheet = out.new_page(width=A4_LANDSCAPE.width, height=A4_LANDSCAPE.height)
    used = set()
    for spec in args.place:
        pos, source, pno, crop, rot = parse_place(spec)
        if pos in used:
            sys.exit(f"position {pos} used twice")
        used.add(pos)
        doc = load_page(source, pno)
        page = doc[0]
        clip = page.rect if crop == "full" else mm_rect(*map(float, crop.split(",")))
        clip &= page.rect
        target = mm_rect(*LABELS_MM[pos])
        target = target + (INSET_MM * MM, INSET_MM * MM, -INSET_MM * MM, -INSET_MM * MM)
        if rot == "auto":
            # Rotate when the crop's orientation differs from the label's (landscape).
            rot = 90 if clip.height > clip.width else 0
        rot = int(rot)
        sheet.show_pdf_page(target, doc, 0, clip=clip, rotate=rot, keep_proportion=True)
        w, h = (clip.height, clip.width) if rot in (90, 270) else (clip.width, clip.height)
        scale = min(target.width / w, target.height / h)
        print(f"{pos}: {source} p{pno} crop {fmt(clip)} mm, rot {rot}, scale {scale:.0%}")
    out_path = Path(args.out)
    out.save(out_path, garbage=3, deflate=True)
    print(f"saved {out_path}")
    if args.preview:
        # Preview only: label outlines drawn on a copy, never in the PDF to print.
        prev = pymupdf.open(out_path)
        pg = prev[0]
        for box in LABELS_MM.values():
            pg.draw_rect(mm_rect(*box), color=(0.6, 0.6, 0.6), width=0.5)
        pg.get_pixmap(dpi=80).save(args.preview)
        print(f"preview {args.preview}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("inspect")
    i.add_argument("source")
    i.add_argument("--page", type=int)
    i.add_argument("--out", default=".")
    b = sub.add_parser("build")
    b.add_argument("--out", required=True)
    b.add_argument("--place", action="append", required=True)
    b.add_argument("--preview", help="PNG path for a preview with label outlines")
    args = p.parse_args()
    inspect(args) if args.cmd == "inspect" else build(args)


if __name__ == "__main__":
    main()
