from fastapi import Request

from app.services import WeatherService


def get_weather_service(request: Request) -> WeatherService:
    """Fournit le WeatherService créé au démarrage (voir lifespan dans app/main.py)."""
    return request.app.state.weather_service
