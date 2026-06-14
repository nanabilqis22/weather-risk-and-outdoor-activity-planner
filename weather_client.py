import urllib.request
import json

class Forecast:
    def __init__(self, temperature: float, condition: str, humidity: int, wind_speed: float):
        self.temperature = temperature
        self.condition = condition
        self.humidity = humidity
        self.wind_speed = wind_speed

class WeatherClient:
    def fetch_forecast(self, location: str) -> Forecast:
        """
        Fetches live data from Open-Meteo's public API.
        Applies exception handling for network or location errors.
        """
        # Clean the location string using standard replacement rules
        city = location.strip().replace(" ", "+")
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        
        try:
            # 1. Geocoding API Request
            with urllib.request.urlopen(geo_url, timeout=10) as response:
                geo_data = json.loads(response.read().decode())
                
            if not geo_data.get("results"):
                raise ValueError(f"Location '{location}' could not be found by the weather service.")
                
            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            
            # 2. Weather Forecast API Request
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&relative_humidity_2m=true"
            with urllib.request.urlopen(weather_url, timeout=10) as response:
                weather_data = json.loads(response.read().decode())
                
            current = weather_data["current_weather"]
            weather_code = current.get("weathercode", 0)
            
            # Map numeric weather codes to clean descriptions
            condition = "Clear Sky"
            if weather_code in [1, 2, 3]: condition = "Partly Cloudy"
            elif weather_code in [45, 48]: condition = "Foggy"
            elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]: condition = "Rainy"
            elif weather_code in [95, 96, 99]: condition = "Thunderstorm"

            return Forecast(
                temperature=float(current["temperature"]),
                condition=condition,
                humidity=int(weather_data.get("current_weather_units", {}).get("relative_humidity_2m", 65)),
                wind_speed=float(current["windspeed"])
            )
            
        except urllib.error.URLError:
            raise RuntimeError("Network Error: Unable to connect to the weather service internet server.")
        except json.JSONDecodeError:
            raise RuntimeError("Data Error: Server returned an unreadable response format.")