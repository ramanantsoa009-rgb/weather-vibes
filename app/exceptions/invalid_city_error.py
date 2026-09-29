from app.exceptions.weather_vibes_error import WeatherVibesError


class InvalidCityError(WeatherVibesError):
    status_code = 400
    default_message = "Merci d'indiquer un nom de ville."
