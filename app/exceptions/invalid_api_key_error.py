from app.exceptions.weather_vibes_error import WeatherVibesError


class InvalidApiKeyError(WeatherVibesError):
    status_code = 502
    default_message = "Clé API OpenWeatherMap invalide ou pas encore activée."
