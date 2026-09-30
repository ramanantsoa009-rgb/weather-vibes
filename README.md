# Weather Vibes

Petite application web météo : on tape une ville, elle affiche la météo actuelle accompagnée d'une "vibe" (un thème visuel et un message adapté au temps qu'il fait).

Démo en ligne : https://weather-vibes-alpha.vercel.app/

L'application est volontairement simple. Le vrai but du projet est de **pratiquer une chaîne de déploiement complète sur Kubernetes** : conteneurisation, CI avec Tekton, déploiement GitOps avec ArgoCD, et gestion des secrets avec Sealed Secrets.

## En bref

| Élément        | Choix                                                  |
| -------------- | ------------------------------------------------------ |
| Backend        | Python, FastAPI, httpx                                 |
| Frontend       | HTML (Jinja2), CSS et JavaScript sans framework        |
| Données météo  | API OpenWeatherMap (clé gratuite requise)              |
| Conteneur      | Docker (image `python:3.12-slim`)                      |
| Registre       | Docker Hub, `adriendockeraccount/weather-vibes`        |
| CI             | Tekton (clone, build Kaniko, mise à jour du manifest)  |
| CD             | ArgoCD, qui synchronise le dossier `k8s/`              |
| Secrets        | Sealed Secrets (Bitnami)                               |

## Fonctionnement de l'application

1. Le navigateur charge la page `/` et envoie la ville saisie à `GET /weather?city=...`.
2. Le backend interroge OpenWeatherMap (unités métriques, langue française).
3. La condition météo (Clear, Rain, Snow...) est traduite en "vibe" par `VibeMapper` : un thème (`sunny`, `rainy`, `night`...) et un message.
4. Le frontend applique le thème (fond, illustration SVG) et affiche le résultat. La dernière ville consultée est mémorisée dans le navigateur.

Routes exposées :

- `GET /` : la page web
- `GET /weather?city=Paris` : la météo en JSON
- `GET /health` : sonde de santé pour Kubernetes
- `GET /docs` : documentation interactive générée par FastAPI

## Lancer en local

Prérequis : Python 3.9 ou plus récent, et une clé API OpenWeatherMap (https://home.openweathermap.org/api_keys).

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # puis renseigner OPENWEATHER_API_KEY dans .env

uvicorn app.main:app --reload
```

L'application est alors disponible sur http://localhost:8000.

Avec Docker :

```bash
docker build -t weather-vibes .
docker run -p 8000:8000 --env-file .env weather-vibes
```

## Chaîne CI/CD

```
 git push (main)
      |
      v
 Tekton PipelineRun  (lancé manuellement : kubectl create -f tekton/pipeline-run.yaml)
      |
      |-- 1. clone            récupère le dépôt GitHub
      |-- 2. build-push       Kaniko construit l'image et la pousse sur Docker Hub,
      |                       taguée avec le hash du commit
      |-- 3. update-manifest  remplace le tag d'image dans k8s/deployment.yaml
      |                       et pousse un commit "ci: deploy ... [skip ci]"
      v
 Dépôt GitHub (dossier k8s/ modifié)
      |
      v
 ArgoCD détecte le changement et synchronise le cluster
      |
      v
 Deployment weather-vibes (2 réplicas), exposé en NodePort 30090
```

Le tag d'image est toujours le hash du commit source : on sait exactement quel code tourne dans le cluster.

Les tâches `git-clone` et `kaniko` proviennent du catalogue Tekton (Tekton Hub) et doivent être installées dans le cluster ; elles ne sont pas dans ce dépôt. L'application ArgoCD elle-même est configurée directement dans le cluster.

## Gestion des secrets

Aucun secret n'est stocké en clair dans le dépôt.

| Secret                | Usage                                  | Où il vit                                                                 |
| --------------------- | -------------------------------------- | ------------------------------------------------------------------------- |
| `OPENWEATHER_API_KEY` | Appels à OpenWeatherMap                | En local : `.env` (ignoré par Git). Dans le cluster : `k8s/sealed-secret.yaml.yaml` |
| `dockerhub-secret`    | Push de l'image par Kaniko             | Créé à la main dans le cluster (`tekton/dockerhub-secret.yaml`, ignoré par Git) |
| `github-token`        | Push du commit de mise à jour du manifest | Créé à la main dans le cluster                                          |

Le SealedSecret est chiffré avec la clé publique du contrôleur Sealed Secrets du cluster : il peut être commité sans risque, et seul ce cluster peut le déchiffrer. Pour changer la clé API :

```bash
kubectl create secret generic weather-secret \
  --from-literal=openweather-api-key=NOUVELLE_CLE \
  --dry-run=client -o yaml \
  | kubeseal --format yaml > k8s/sealed-secret.yaml.yaml
```

Puis commiter le fichier : ArgoCD applique le nouveau secret, et les pods le prennent en compte à leur redémarrage.

## Structure du projet

```
app/
  main.py          point d'entrée : assemble configuration, services et routes
  config.py        paramètres lus depuis les variables d'environnement
  api/             routes HTTP (pages, weather, health) et gestion des erreurs
  services/        client OpenWeatherMap, logique métier, association météo -> vibe
  models/          modèles de données (WeatherReport, Vibe)
  exceptions/      erreurs métier, chacune associée à un code HTTP
  templates/       page HTML
  static/          CSS, JavaScript et illustrations SVG par type de météo
k8s/               manifests Kubernetes surveillés par ArgoCD
tekton/            pipeline CI et ses tâches
Dockerfile
requirements.txt
.env.example       modèle du fichier .env
```

## Pour s'y retrouver plus tard

- Pour ajouter ou modifier une vibe, tout se passe dans `app/services/vibe_mapper.py`.
- Si l'application renvoie une erreur de clé API, vérifier `.env` en local, ou le secret `weather-secret` dans le cluster.
- Le SealedSecret n'est valable que pour le cluster qui l'a chiffré. Sur un nouveau cluster, il faut le régénérer avec `kubeseal`.
- Les commits `ci: deploy ...` sont créés automatiquement par le pipeline. Penser à faire `git pull` avant de travailler.
