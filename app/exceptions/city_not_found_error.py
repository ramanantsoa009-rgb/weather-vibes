from app.exceptions.weather_vibes_error import WeatherVibesError


class CityNotFoundError(WeatherVibesError):
    status_code = 404

    def __init__(self, city: str) -> None:
        super().__init__(f"Ville introuvable : « {city} ».")
