from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_weather_service
from app.models import WeatherReport
from app.services import WeatherService

router = APIRouter()


@router.get("/weather", response_model=WeatherReport)
async def get_weather(
    city: str = Query(..., min_length=1, max_length=100, description="Nom de la ville"),
    service: WeatherService = Depends(get_weather_service),
) -> WeatherReport:
    return await service.get_weather(city)
