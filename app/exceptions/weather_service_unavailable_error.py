from app.exceptions.weather_vibes_error import WeatherVibesError


class WeatherServiceUnavailableError(WeatherVibesError):
    status_code = 503
    default_message = "Service météo injoignable pour le moment."
