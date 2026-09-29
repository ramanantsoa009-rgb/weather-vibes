"""Cas d'usage principal : obtenir la météo d'une ville et l'enrichir avec sa vibe."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from app.exceptions import InvalidCityError, InvalidWeatherResponseError
from app.models import WeatherReport
from app.services.openweather_client import OpenWeatherClient
from app.services.vibe_mapper import VibeMapper

logger = logging.getLogger(__name__)

_METERS_PER_SECOND_TO_KMH = 3.6


class WeatherService:
    def __init__(self, client: OpenWeatherClient, vibe_mapper: VibeMapper) -> None:
        self._client = client
        self._vibe_mapper = vibe_mapper

    async def get_weather(self, city: str) -> WeatherReport:
        city = city.strip()
        if not city:
            raise InvalidCityError()

        raw_weather = await self._client.fetch_current_weather(city)
        try:
            return self._to_report(raw_weather)
        except (KeyError, IndexError, TypeError) as exc:
            logger.exception("Réponse OpenWeatherMap illisible")
            raise InvalidWeatherResponseError() from exc

    def _to_report(self, data: Dict[str, Any]) -> WeatherReport:
        weather = data["weather"][0]
        measures = data["main"]
        condition = weather.get("main", "")

        return WeatherReport(
            city=data.get("name", ""),
            country=data.get("sys", {}).get("country"),
            temperature=round(measures["temp"], 1),
            feels_like=_round_or_none(measures.get("feels_like")),
            description=weather.get("description", ""),
            condition=condition,
            humidity=measures.get("humidity"),
            wind=_to_kmh(data.get("wind", {}).get("speed")),
            vibe=self._vibe_mapper.to_vibe(condition, weather.get("icon", "")),
        )


def _round_or_none(value: Optional[float]) -> Optional[float]:
    return round(value, 1) if value is not None else None


def _to_kmh(speed_ms: Optional[float]) -> Optional[float]:
    return round(speed_ms * _METERS_PER_SECOND_TO_KMH, 1) if speed_ms is not None else None
