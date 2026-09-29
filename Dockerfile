# Image de base : Python léger
FROM python:3.12-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Copier d'abord les dépendances (optimisation du cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY app/ ./app/

# Documenter le port utilisé
EXPOSE 8000

# Lancer l'appli (host 0.0.0.0 = crucial pour le conteneur !)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]