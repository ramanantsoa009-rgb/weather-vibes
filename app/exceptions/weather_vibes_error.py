from __future__ import annotations

from typing import Optional


class WeatherVibesError(Exception):
    """Erreur métier de base. Chaque sous-classe définit son code HTTP et son message."""

    status_code: int = 500
    default_message: str = "Une erreur inattendue est survenue."

    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)
