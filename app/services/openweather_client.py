"""Accès HTTP à l'API OpenWeatherMap. Traduit les erreurs réseau et HTTP en erreurs métier."""

from __future__ import annotations

import logging
from typing import Any, Dict

import httpx

from app.config import Settings
from app.exceptions import (
    CityNotFoundError,
    InvalidApiKeyError,
    InvalidWeatherResponseError,
    MissingApiKeyError,
    WeatherServiceTimeoutError,
    WeatherServiceUnavailableError,
)

logger = logging.getLogger(__name__)


class OpenWeatherClient:
    def __init__(self, http_client: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http_client
        self._settings = settings

    async def fetch_current_weather(self, city: str) -> Dict[str, Any]:
        response = await self._send_request(city)
        self._raise_for_status(response, city)
        return self._decode_json(response)

    async def _send_request(self, city: str) -> httpx.Response:
        params = {
            "q": city,
            "appid": self._require_api_key(),
            "units": self._settings.UNITS,
            "lang": self._settings.LANGUAGE,
        }
        try:
            return await self._http.get(self._settings.OPENWEATHER_URL, params=params)
        except httpx.TimeoutException as exc:
            raise WeatherServiceTimeoutError() from exc
        except httpx.HTTPError as exc:
            logger.warning("Erreur réseau vers OpenWeatherMap : %s", type(exc).__name__)
            raise WeatherServiceUnavailableError() from exc

    def _require_api_key(self) -> str:
        api_key = self._settings.openweather_api_key
        if not api_key:
            raise MissingApiKeyError()
        return api_key

    @staticmethod
    def _raise_for_status(response: httpx.Response, city: str) -> None:
        status = response.status_code
        if status == 200:
            return
        if status == 404:
            raise CityNotFoundError(city)
        if status == 401:
            raise InvalidApiKeyError()
        if status == 429:
            raise WeatherServiceUnavailableError("Trop de requêtes vers le service météo, réessaie plus tard.")
        logger.warning("Réponse inattendue d'OpenWeatherMap : HTTP %s", status)
        raise InvalidWeatherResponseError()

    @staticmethod
    def _decode_json(response: httpx.Response) -> Dict[str, Any]:
        try:
            return response.json()
        except ValueError as exc:
            raise InvalidWeatherResponseError() from exc
