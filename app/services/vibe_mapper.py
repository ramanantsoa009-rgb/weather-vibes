"""Associe une condition météo OpenWeatherMap (Clear, Rain, Snow…) à une vibe."""

from __future__ import annotations

from typing import Dict

from app.models import Vibe

_VIBES_BY_CONDITION: Dict[str, Vibe] = {
    "Clear": Vibe(emoji="☀️", theme="sunny", message="Belle journée, profites-en ! ✨"),
    "Clouds": Vibe(emoji="☁️", theme="cloudy", message="Un peu nuageux aujourd'hui, mais ça reste cosy~"),
    "Rain": Vibe(emoji="🌧️", theme="rainy", message="N'oublie pas ton parapluie ! ☂️"),
    "Drizzle": Vibe(emoji="🌦️", theme="rainy", message="Petite bruine en approche, capuche conseillée !"),
    "Thunderstorm": Vibe(emoji="⛈️", theme="storm", message="Orage ! Reste à l'abri avec un bon thé 🍵"),
    "Snow": Vibe(emoji="❄️", theme="snowy", message="Il neige, reste au chaud sous un plaid !"),
    "Mist": Vibe(emoji="🌫️", theme="foggy", message="Visibilité réduite, prudence."),
    "Fog": Vibe(emoji="🌫️", theme="foggy", message="Brouillard mystérieux… avance doucement."),
    "Haze": Vibe(emoji="🌫️", theme="foggy", message="Ciel voilé, ambiance rêveuse."),
    "Smoke": Vibe(emoji="🌫️", theme="foggy", message="Air enfumé, limite les efforts dehors."),
    "Dust": Vibe(emoji="🌪️", theme="foggy", message="Poussière dans l'air, protège tes yeux !"),
    "Sand": Vibe(emoji="🏜️", theme="foggy", message="Vent de sable, garde tes lunettes !"),
    "Ash": Vibe(emoji="🌋", theme="storm", message="Cendres volcaniques ! Reste à l'intérieur."),
    "Squall": Vibe(emoji="💨", theme="storm", message="Bourrasques ! Tiens bien ton chapeau."),
    "Tornado": Vibe(emoji="🌪️", theme="storm", message="Tornade ! Mets-toi en sécurité immédiatement."),
}
_CLEAR_NIGHT_VIBE = Vibe(emoji="🌙", theme="night", message="Nuit claire, parfaite pour compter les étoiles ⭐")
_DEFAULT_VIBE = Vibe(emoji="🌈", theme="default", message="Météo mystère du jour.")

_NIGHT_ICON_SUFFIX = "n"  # les icônes OpenWeatherMap finissent par "n" la nuit (ex. "01n")


class VibeMapper:
    def to_vibe(self, condition: str, icon: str = "") -> Vibe:
        if condition == "Clear" and icon.endswith(_NIGHT_ICON_SUFFIX):
            return _CLEAR_NIGHT_VIBE
        return _VIBES_BY_CONDITION.get(condition, _DEFAULT_VIBE)
