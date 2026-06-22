import requests
from forecast import Forecast


class WeatherClient:

    def get_coordinates(self, location):
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}"

        response = requests.get(url)
        data = response.json()

        if "results" not in data:
            raise Exception("Location not found")

        result = data["results"][0]

        return result["latitude"], result["longitude"]

    def get_weather(self, location):
        lat, lon = self.get_coordinates(location)

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,wind_speed_10m,precipitation"
        )

        response = requests.get(url)
        data = response.json()

        temp = data["current"]["temperature_2m"]
        wind = data["current"]["wind_speed_10m"]
        rain = data["current"]["precipitation"]

        return Forecast(
            temperature=temp,
            wind_speed=wind,
            precipitation=rain
        )
