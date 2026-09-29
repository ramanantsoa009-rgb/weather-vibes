"""Configuration de l'application, lue depuis les variables d'environnement."""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv

# En local, charge le fichier .env s'il existe. Une variable déjà définie
# (ex. injectée par un Secret Kubernetes) n'est jamais écrasée.
load_dotenv()


class Settings:
    """Paramètres de l'application. Aucune valeur secrète n'est codée en dur."""

    OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
    UNITS = "metric"
    LANGUAGE = "fr"
    REQUEST_TIMEOUT_SECONDS = 5.0
    CONNECT_TIMEOUT_SECONDS = 3.0

    @property
    def openweather_api_key(self) -> Optional[str]:
        # Lue à chaque appel : une rotation du Secret est prise en compte au redémarrage du pod.
        return os.environ.get("OPENWEATHER_API_KEY")
