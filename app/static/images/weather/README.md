# Illustrations météo

Une illustration SVG animée par thème, affiché au-dessus de la température. Nom de fichier = thème renvoyé par l'API (`vibe.theme`) :

| Fichier       | Météo                                      |
|---------------|--------------------------------------------|
| `sunny.svg`   | ciel dégagé (jour)                         |
| `night.svg`   | ciel dégagé (nuit)                         |
| `cloudy.svg`  | nuageux                                    |
| `rainy.svg`   | pluie, bruine                              |
| `storm.svg`   | orage, bourrasques, tornade, cendres       |
| `snowy.svg`   | neige                                      |
| `foggy.svg`   | brume, brouillard, poussière, sable        |
| `default.svg` | toute autre condition                      |

Conseils : carré (viewBox 256×256, affiché en 170×170), fond transparent, animation en CSS interne au SVG (`<style>` + `@keyframes`). Pas de `<script>` ni de ressource externe : un SVG chargé via `<img>` ne les exécute pas.
Si un fichier manque, rien n'est affiché à cet endroit (pas d'erreur).
