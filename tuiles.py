"""Découpe la carte Farental en tuiles XYZ (256 px) pour uMap / Leaflet.

L'image est posée au centre du monde Web Mercator, à sa taille réelle au zoom NATIF.
Zooms plus petits : image réduite ; zooms plus grands : image agrandie.
Les tuiles à moitié hors de l'image sont complétées avec la couleur du bord.
"""
import json
import math
import sys
from pathlib import Path

from PIL import Image

SOURCE = Path(sys.argv[1])
SORTIE = Path(sys.argv[2])
NATIF, ZMIN, ZMAX = 3, 1, 5
T = 256

img = Image.open(SOURCE).convert("RGB")
W, H = img.size
fond = img.getpixel((2, 2))

monde = T * 2 ** NATIF
ox, oy = (monde - W) / 2, (monde - H) / 2  # coin haut-gauche de l'image au zoom natif


def latlng(px, py, z):
    n = T * 2 ** z
    lng = px / n * 360 - 180
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * py / n))))
    return lat, lng


total = 0
for z in range(ZMIN, ZMAX + 1):
    s = 2 ** (z - NATIF)
    iw, ih = round(W * s), round(H * s)
    x0, y0 = round(ox * s), round(oy * s)
    redim = img.resize((iw, ih), Image.LANCZOS)
    for tx in range(x0 // T, (x0 + iw - 1) // T + 1):
        for ty in range(y0 // T, (y0 + ih - 1) // T + 1):
            tuile = Image.new("RGB", (T, T), fond)
            tuile.paste(redim, (x0 - tx * T, y0 - ty * T))
            dossier = SORTIE / str(z) / str(tx)
            dossier.mkdir(parents=True, exist_ok=True)
            tuile.save(dossier / f"{ty}.jpg", quality=88, optimize=True)
            total += 1

nord, ouest = latlng(ox, oy, NATIF)
sud, est = latlng(ox + W, oy + H, NATIF)
centre = latlng(ox + W / 2, oy + H / 2, NATIF)
info = {
    "tuiles": total,
    "zoom_min": ZMIN,
    "zoom_max": ZMAX,
    "zoom_natif": NATIF,
    "limites": {"nord": round(nord, 4), "sud": round(sud, 4), "ouest": round(ouest, 4), "est": round(est, 4)},
    "centre": {"lat": round(centre[0], 4), "lng": round(centre[1], 4)},
    "couleur_fond": "#%02x%02x%02x" % fond,
}
(SORTIE / "info.json").write_text(json.dumps(info, indent=2, ensure_ascii=False))
print(json.dumps(info, indent=2, ensure_ascii=False))
