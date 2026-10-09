"""Génère les couches GeoJSON de la carte Farental pour uMap.

Les positions sont en pixels de l'image farental.jpg (1376 x 768),
converties dans les coordonnées fictives utilisées par les tuiles (voir tuiles.py).
"""
import json
import math
import sys
from pathlib import Path

N = 256 * 2**3            # largeur du monde au zoom natif (3)
OX, OY = (N - 1376) / 2, (N - 768) / 2


def ll(px, py):
    """Pixel de l'image -> [lng, lat] (ordre GeoJSON)."""
    X, Y = OX + px, OY + py
    lng = X / N * 360 - 180
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * Y / N))))
    return [round(lng, 5), round(lat, 5)]


def point(nom, px, py, description, couleur, picto=None):
    opts = {"color": couleur, "iconClass": "Default"}
    if picto:
        opts["iconUrl"] = picto
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": ll(px, py)},
        "properties": {"name": nom, "description": description, "_umap_options": opts},
    }


def route(nom, points, description, couleur, pointilles=False):
    opts = {"color": couleur, "weight": 5, "opacity": 0.85}
    if pointilles:
        opts["dashArray"] = "8,8"
    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": [ll(x, y) for x, y in points]},
        "properties": {"name": nom, "description": description, "_umap_options": opts},
    }


MARRON, BLEU, ROUGE, VERT, OR = "SaddleBrown", "RoyalBlue", "Crimson", "ForestGreen", "Goldenrod"

villes = [
    point("Horten'taar", 680, 362,
          "**Type :** Ville principale centrale (capitale)\n"
          "**Bâtiments & commodités :** Hôtel de ville, Banque, Boîte aux lettres, Marché, Taverne, Port\n"
          "**Métiers :** Atelier Forgeron, Atelier Armurier\n"
          "**Ressources (pêche au port) :** Crabe à pinces dures, Crevette grise, Hareng argenté\n"
          "**Géographie :** Point central de la carte, dessert toutes les régions.",
          OR),
    point("Martel", 240, 382,
          "**Type :** Ville de l'Ouest\n"
          "**Bâtiments & commodités :** Banque, Boîte aux lettres, Taverne\n"
          "**Métiers :** Atelier Mineur, Atelier Joaillier\n"
          "**Zones adjacentes :** Mines de Martel, Champs de Martel",
          MARRON),
    point("Balanol", 240, 566,
          "**Type :** Ville du Sud-Ouest\n"
          "**Bâtiments & commodités :** Banque, Boîte aux lettres, Taverne\n"
          "**Métiers :** Atelier Couturier, Atelier Sculpteur\n"
          "**Zones adjacentes :** Étang de Balanol, Clairière de Balanol",
          MARRON),
    point("Venor'taar", 1105, 382,
          "**Type :** Ville de l'Est\n"
          "**Bâtiments & commodités :** Banque, Boîte aux lettres, Taverne\n"
          "**Métiers :** Atelier Bûcheron, Atelier Alchimiste\n"
          "**Zones adjacentes :** Petite Forêt, Cavernes de V., Fermes de Venor'taar",
          MARRON),
]

ressources = [
    point("Port d'Horten'taar", 680, 190,
          "**Pêche :** Crabe à pinces dures, Crevette grise, Hareng argenté",
          BLEU),
    point("Mines de Martel", 165, 212,
          "**Ressources :** Minerai de fer, Charbon, Étain",
          MARRON),
    point("Champs de Martel", 300, 255,
          "**Ressources :** Blé doré, Orge sauvage\n**Monstres :** Épouvantail animé",
          VERT),
    point("Étang de Balanol", 185, 705,
          "**Pêche :** Têtard pointu, Brochet majestueux",
          BLEU),
    point("Clairière de Balanol", 360, 690,
          "**Ressources :** Herbe médicinale, Fleur de lin\n**Monstres :** Loup des bois",
          VERT),
    point("Petite Forêt", 1000, 258,
          "**Ressources :** Bois de chêne, Bois de bouleau\n**Monstres :** Araignée tisseuse",
          VERT),
    point("Fermes de Venor'taar", 1080, 548,
          "**Ressources :** Laine de mouton, Cuir brut",
          VERT),
]

dangers = [
    point("Cavernes de V.", 1228, 205,
          "**Cavernes de Venor'taar**\n"
          "**Ressources :** Cristaux de mana, Pierre brute\n**Monstres :** Chauve-souris géante",
          ROUGE),
    point("Camp de bandit", 965, 605,
          "**Zone hostile :** aggro fréquente de Bandits",
          ROUGE),
]

routes = [
    route("Route de Martel (Horten'taar ➔ Martel)",
          [(625, 372), (520, 370), (400, 371), (275, 384)],
          "**Temps à pied :** 4 min 30 s\n**Risques :** Zone sécurisée, quelques sangliers bas niveau.",
          VERT),
    route("Martel ➔ Balanol",
          [(243, 400), (245, 470), (243, 548)],
          "**Temps à pied :** 3 min 15 s\n**Risques :** Route forestière, attention aux brigands la nuit.",
          OR),
    route("Route de Venor'taar (Horten'taar ➔ Venor'taar)",
          [(740, 372), (850, 372), (970, 373), (1075, 378)],
          "**Temps à pied :** 5 min 10 s\n**Risques :** Longue route sinueuse, traversée de ponts.",
          OR),
    route("Horten'taar ➔ Port d'Horten'taar",
          [(680, 318), (680, 260), (680, 215)],
          "**Temps à pied :** 1 min 00 s\n**Risques :** Axe commercial direct et 100 % sécurisé.",
          VERT),
    route("Venor'taar ➔ Camp de bandit",
          [(1090, 400), (1050, 460), (1015, 530), (985, 590)],
          "**Temps à pied :** 2 min 45 s\n**Risques :** Zone hostile (aggro fréquente de Bandits).",
          ROUGE, pointilles=True),
]

sortie = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
couches = {"villes": villes, "ressources": ressources, "dangers": dangers, "routes": routes}
for nom, feats in couches.items():
    (sortie / f"{nom}.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False, indent=1))
    print(nom, len(feats))
