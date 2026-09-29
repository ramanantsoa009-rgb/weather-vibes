from app.exceptions.weather_vibes_error import WeatherVibesError


class InvalidWeatherResponseError(WeatherVibesError):
    status_code = 502
    default_message = "Le service météo a renvoyé une réponse inattendue."
