#!/usr/bin/env python3
"""Resize and convert job photos for the website (one-off; needs Pillow).

    python3 scripts/prep_photos.py /path/to/Komo-Website-Photos

Writes 3:4 portrait WebP files at two widths into src/assets/img/, with all
metadata (EXIF, GPS) stripped. Lighting/interior shots use the retouched
versions; equipment close-ups use the unedited originals so labels stay true.
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent.parent / "src" / "assets" / "img"
WIDTHS = (480, 900)

PICKS = {
    "electrician-at-work": "Edited-JPG/04-electrician-at-work.jpg",
    "chandelier-feature-lighting": "Edited-JPG/07-chandelier-feature-lighting.jpg",
    "linear-ceiling-lighting": "Edited-JPG/08-architectural-linear-lighting.jpg",
    "bakery-fit-out": "Edited-JPG/09-bakery-interior.jpg",
    "restaurant-counter-lighting": "Edited-JPG/14-restaurant-counter-lighting.jpg",
    "restaurant-dining-lighting": "Edited-JPG/15-restaurant-dining-lighting.jpg",
    "residential-recessed-lighting": "Edited-JPG/16-residential-recessed-lighting.jpg",
    "track-lighting-install": "Edited-JPG/17-commercial-track-lighting.jpg",
    "exposed-conduit-lighting": "Edited-JPG/18-exposed-conduit-lighting.jpg",
    "residential-panel": "Original-Facebook-Photos/00-residential-panel.jpg",
    "fused-disconnect": "Original-Facebook-Photos/01-commercial-switchgear.jpg",
    "commercial-panel": "Original-Facebook-Photos/02-commercial-panel.jpg",
    "control-panel": "Original-Facebook-Photos/05-control-cabinet.jpg",
    "distribution-panel": "Original-Facebook-Photos/10-distribution-panel.jpg",
    "motor-contactors": "Original-Facebook-Photos/13-motor-contactors.jpg",
}

OUT.mkdir(parents=True, exist_ok=True)
for name, rel in PICKS.items():
    im = ImageOps.exif_transpose(Image.open(SRC / rel)).convert("RGB")
    im = ImageOps.fit(im, (im.width, round(im.width * 4 / 3)) if im.height / im.width > 4 / 3 else (round(im.height * 3 / 4), im.height))
    for w in WIDTHS:
        w2 = min(w, im.width)
        out = im.resize((w2, round(w2 * 4 / 3)), Image.LANCZOS)
        out.save(OUT / f"{name}-{w}.webp", "WEBP", quality=78, method=6)  # no exif passed: metadata stripped
    print(name, im.size)
