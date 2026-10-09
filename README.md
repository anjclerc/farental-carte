# Carte de Farental — tuiles pour uMap

Carte du jeu [Farental](https://farental.ch) découpée en tuiles 256 px (format XYZ) pour l'afficher comme fond de carte dans [uMap](https://umap.openstreetmap.fr) ou Leaflet.

## Adresse à coller dans uMap

*Propriétés avancées de la carte → Custom background → url* :

```
https://cdn.jsdelivr.net/gh/anjclerc/farental-carte@main/tuiles/{z}/{x}/{y}.jpg
```

| Réglage | Valeur |
|---|---|
| Zoom min | 1 |
| Zoom max | 5 |
| Zoom de départ conseillé | 3 (taille réelle de l'image) |
| Centre | lat 0, lng 0 |
| Limites (nord, sud, ouest, est) | 55.7766, -55.7766, -120.9375, 120.9375 |

L'image est posée au centre du monde Web Mercator : les coordonnées sont fictives, elles servent seulement à placer la carte.

## Régénérer les tuiles

```bash
python3 tuiles.py farental.jpg tuiles   # nécessite Pillow
```

`tuiles/info.json` donne les limites et les zooms calculés. Après une mise à jour, le cache de jsDelivr peut garder l'ancienne version quelques heures ; on peut le vider sur https://www.jsdelivr.com/tools/purge.
