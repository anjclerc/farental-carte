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

# Sources : le jeu (pages Lieu, Voyage, Journal, 07.10.2026) et les schémas de la
# communauté. Format des descriptions : une ligne « **Rubrique :** valeurs » par
# information, valeurs séparées par des virgules. Les durées sont celles du jeu.
# « À vérifier » signale un écart entre les sources.

villes = [
    point("Horten'taar", 680, 362,
          "**Type :** Capitale · Colline\n"
          "**Installations :** Banque, Boîte aux lettres, Forge, Marchand, Relais de voyage, Taverne\n"
          "**Métiers :** Mage, Sculpteur, Travailleur du cuir\n"
          "**Trajets :** Port d'Horten'taar 15 min, Fermes d'Horten'taar 15 min, Scierie d'Horten'taar 15 min\n"
          "**Relais :** Martel 15 min (350 G), Venor'taar 15 min (350 G)",
          OR),
    point("Martel", 240, 382,
          "**Type :** Village · Colline\n"
          "**Installations :** Boîte aux lettres, Fonderie, Forge, Intendant des terres, Marchand, Relais de voyage, Taverne, École de forge\n"
          "**Métiers :** Forgeron, Mineur, Travailleur du cuir\n"
          "**Trajets :** Champs de Martel 15 min, Mine de Martel 30 min, Fermes d'Horten'taar 45 min, Balanol 1 h\n"
          "**Relais :** Horten'taar 15 min (350 G), Venor'taar 30 min (700 G)\n"
          "**Activités :** Travailler à la taverne, Apprendre les bases de la forge",
          MARRON),
    point("Balanol", 240, 566,
          "**Type :** Ville · Forêt\n"
          "**Installations :** Banque, Boîte aux lettres, Marchand, Relais de voyage, Taverne, Scierie, Laboratoire d'alchimie\n"
          "**Métiers :** Couturier, Sculpteur, Travailleur du cuir, Alchimiste\n"
          "**Trajets :** Étang de Balanol 15 min, Clairière de Balanol 30 min, Martel 1 h\n"
          "**Relais :** Venor'taar 45 min (1050 G)",
          MARRON),
    point("Venor'taar", 1105, 382,
          "**Type :** Village · Champ\n"
          "**Installations :** Boîte aux lettres, Laboratoire d'alchimie, Marchand, Relais de voyage, Taverne, École d'alchimie\n"
          "**Métiers :** Alchimiste\n"
          "**Trajets :** Petite forêt de Venor'taar 15 min, Cavernes de Venor'taar 15 min, Fermes de Venor'taar 15 min, Camp de bandit 45 min, Scierie d'Horten'taar 45 min\n"
          "**Relais :** Horten'taar 15 min (350 G), Martel 30 min (700 G), Balanol 45 min (1050 G)",
          MARRON),
]

ressources = [
    point("Port d'Horten'taar", 680, 190,
          "**Type :** Nature sauvage · Colline · Rivière\n"
          "**Installations :** Port, Boîte aux lettres, Marchand, Taverne, Activité illégale\n"
          "**Activités :** Entraînement guerrier, Entraînement au tir à l'arc, Travail au port (1,35 G/min)\n"
          "**Pêche :** Rivière\n"
          "**Trajets :** Horten'taar 15 min, Scierie d'Horten'taar 15 min",
          BLEU),
    point("Fermes d'Horten'taar", 540, 290,
          "**Type :** Nature sauvage · Colline · Rivière\n"
          "**Trajets :** Horten'taar 15 min, Scierie d'Horten'taar 30 min, Martel 45 min\n"
          "**À compléter :** ressources et monstres",
          VERT),
    point("Scierie d'Horten'taar", 800, 235,
          "**Type :** Nature sauvage · Colline · Rivière\n"
          "**Installations :** Scierie, Atelier de sculpteur\n"
          "**Bûcheron :** Aulneeris torsadé\n"
          "**Trajets :** Horten'taar 15 min, Port d'Horten'taar 15 min, Fermes d'Horten'taar 30 min, Venor'taar 45 min",
          VERT),
    point("Mine de Martel", 165, 212,
          "**Type :** Nature sauvage · Souterrain\n"
          "**Mineur :** Minerai de feerin, Minerai d'oreerin\n"
          "**Activités :** Miner du feerin (8 à 11 minerais par heure)\n"
          "**Trajets :** Martel 30 min\n"
          "**À vérifier :** 30 min dans le jeu, 15 min sur un schéma",
          MARRON),
    point("Champs de Martel", 300, 255,
          "**Type :** Nature sauvage · Champ · Rivière\n"
          "**Pêche :** Rivière\n"
          "**Trajets :** Martel 15 min\n"
          "**À compléter :** ressources et monstres",
          VERT),
    point("Étang de Balanol", 185, 705,
          "**Type :** Nature sauvage · Forêt · Étang · Rivière\n"
          "**Bûcheron :** Lontal touffu, Talafiir pointu, Bralenn majestueux\n"
          "**Pêche :** Étang\n"
          "**Alchimiste :** Pousse de maril, Racine de brol, Fleur de vorliin, Listirelle, Markin sauvage, Velth'aan fine\n"
          "**Monstres :** Jeune oleraan (349), Jeune oleraan + Oleraan adulte (840), Jeune lupiaan (406), Lupiaan adulte (725), Oleraan adulte (491), Oleraan mature (847), Lupiaan féroce (986), Jeune lupiaan + Lupiaan adulte (1131)\n"
          "**PNJ :** Patient fisherman\n"
          "**Trajets :** Balanol 15 min, Grotte des lupiaans 5 min",
          BLEU),
    point("Clairière de Balanol", 360, 690,
          "**Type :** Nature sauvage\n"
          "**Trajets :** Balanol 30 min\n"
          "**À compléter :** ressources et monstres",
          VERT),
    point("Petite forêt de Venor'taar", 1000, 258,
          "**Type :** Nature sauvage · Forêt\n"
          "**Bûcheron :** Lontal touffu, Talafiir pointu\n"
          "**Alchimiste :** Pousse de maril, Racine de brol, Fleur de vorliin\n"
          "**Trajets :** Venor'taar 15 min, Fermes de Venor'taar 15 min",
          VERT),
    point("Cavernes de Venor'taar", 1228, 205,
          "**Type :** Nature sauvage · Souterrain · Lac\n"
          "**Mineur :** Minerai de feerin, Minerai d'oreerin\n"
          "**Pêche :** Lac\n"
          "**Trajets :** Venor'taar 15 min",
          MARRON),
    point("Fermes de Venor'taar", 1080, 548,
          "**Type :** Nature sauvage · Champ · Rivière\n"
          "**Pêche :** Rivière\n"
          "**Alchimiste :** Oreliaar\n"
          "**Monstres :** Jeune oleraan (349), Jeune oleraan + Oleraan adulte (840), Oleraan adulte (491), Oleraan mature (847)\n"
          "**PNJ :** Otho Ghikhaam\n"
          "**Trajets :** Venor'taar 15 min, Petite forêt de Venor'taar 15 min",
          VERT),
]

dangers = [
    point("Camp de bandit des collines du nord", 965, 605,
          "**Type :** Nature sauvage · Colline\n"
          "**Installations :** Atelier de travailleur du cuir, Scierie\n"
          "**Trajets :** Venor'taar 45 min",
          ROUGE),
    point("Grotte des lupiaans", 95, 640,
          "**Type :** Nature sauvage · Souterrain\n"
          "**Mineur :** Minerai de feerin, Minerai d'oreerin, Harkrill\n"
          "**Alchimiste :** Bonnir souterrain\n"
          "**Monstres :** Lupiaan alpha + Jeune lupiaan + Lupiaan féroce (2696)\n"
          "**Trajets :** Étang de Balanol 5 min\n"
          "**À vérifier :** position approximative, absente du fond de carte",
          ROUGE),
]

# Butins connus : Jeune oleraan, Oleraan adulte, Jeune lupiaan → Peau abîmée ;
# Lupiaan adulte, Lupiaan féroce → Peau intacte. Les nombres entre parenthèses
# après les monstres sont la puissance du combat.

routes = [
    route("Route de Martel (Martel ➔ Horten'taar)",
          [(625, 372), (520, 370), (400, 371), (275, 384)],
          "**Durée :** 1 h sans arrêt\n"
          "**Étapes :** Martel ➔ Fermes d'Horten'taar 45 min, Fermes d'Horten'taar ➔ Horten'taar 15 min\n"
          "**Relais :** Martel ⇄ Horten'taar 15 min (350 G)",
          VERT),
    route("Martel ➔ Balanol",
          [(243, 400), (245, 470), (243, 548)],
          "**Durée :** 1 h",
          OR),
    route("Route de Venor'taar (Horten'taar ➔ Venor'taar)",
          [(740, 372), (850, 372), (970, 373), (1075, 378)],
          "**Durée :** 1 h sans arrêt\n"
          "**Étapes :** Horten'taar ➔ Scierie d'Horten'taar 15 min, Scierie d'Horten'taar ➔ Venor'taar 45 min\n"
          "**Relais :** Horten'taar ⇄ Venor'taar 15 min (350 G)",
          OR),
    route("Horten'taar ➔ Port d'Horten'taar",
          [(680, 318), (680, 260), (680, 215)],
          "**Durée :** 15 min",
          VERT),
    route("Venor'taar ➔ Camp de bandit des collines du nord",
          [(1090, 400), (1050, 460), (1015, 530), (985, 590)],
          "**Durée :** 45 min",
          ROUGE, pointilles=True),
]

sortie = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
couches = {"villes": villes, "ressources": ressources, "dangers": dangers, "routes": routes}
for nom, feats in couches.items():
    (sortie / f"{nom}.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False, indent=1))
    print(nom, len(feats))
