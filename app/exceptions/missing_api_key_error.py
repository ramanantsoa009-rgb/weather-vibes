from app.exceptions.weather_vibes_error import WeatherVibesError


class MissingApiKeyError(WeatherVibesError):
    status_code = 500
    default_message = "Clé API absente : la variable d'environnement OPENWEATHER_API_KEY n'est pas définie."
