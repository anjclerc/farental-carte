# Carte de Farental — tuiles pour uMap

Carte du jeu [Farental](https://farental.ch) découpée en tuiles 256 px (format XYZ) pour l'afficher comme fond de carte dans [uMap](https://umap.openstreetmap.fr) ou Leaflet.

## Adresse à coller dans uMap

*Propriétés avancées de la carte → Custom background → url* :

```
https://cdn.jsdelivr.net/gh/anjclerc/farental-carte@a744c2e/tuiles/{z}/{x}/{y}.jpg
```

| Réglage | Valeur |
|---|---|
| Zoom min | 1 |
| Zoom max | 5 |
| Vue par défaut | zoom 2, lat 0, lng 0 (zoom 3 = taille réelle de l'image) |
| Limites (nord, sud, ouest, est) | 55.7766, -55.7766, -120.9375, 120.9375 |

L'image est posée au centre du monde Web Mercator : les coordonnées sont fictives, elles servent seulement à placer la carte.

## Régénérer les tuiles

```bash
python3 tuiles.py farental.jpg tuiles   # nécessite Pillow
```

`tuiles/info.json` donne les limites et les zooms calculés. L'adresse est épinglée sur un commit (`@a744c2e`) : après une nouvelle carte, pousse le commit puis remplace ce code dans uMap par le nouveau (`git log --oneline -1`). Avec `@main`, jsDelivr garde l'ancienne version en cache jusqu'à 12 h.

## Lieux et routes

`donnees/lieux.py` génère les couches GeoJSON importées dans uMap (`villes`, `ressources`, `dangers`, `routes`). Les positions sont données en pixels de `farental.jpg`, le script les convertit dans les coordonnées des tuiles. Import dans uMap : *Import data* → coller le fichier → format *geojson* → *Import in a new layer*.
