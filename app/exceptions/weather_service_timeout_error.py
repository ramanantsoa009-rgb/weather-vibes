from app.exceptions.weather_vibes_error import WeatherVibesError


class WeatherServiceTimeoutError(WeatherVibesError):
    status_code = 504
    default_message = "Le service météo met trop de temps à répondre. Réessaie dans un instant."
