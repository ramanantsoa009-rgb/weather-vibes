from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from app.models.vibe import Vibe


class WeatherReport(BaseModel):
    """Météo actuelle d'une ville, telle que renvoyée par GET /weather."""

    city: str
    country: Optional[str] = None
    temperature: float
    feels_like: Optional[float] = None
    description: str
    condition: str
    humidity: Optional[int] = None
    wind: Optional[float] = None  # km/h
    vibe: Vibe
