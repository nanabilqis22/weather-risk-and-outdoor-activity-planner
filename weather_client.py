import urllib.request
import json

class Forecast:
    def __init__(self, temperature: float, condition: str, humidity: int, wind_speed: float):
        self.temperature = temperature
        self.condition = condition
        self.humidity = humidity
        self.wind_speed = wind_speed

class WeatherClient:
    def __init__(self, api_key: str = ""):
        # We don't strictly need a key for this free open endpoint
        self.api_key = api_key

    def fetch_forecast(self, location: str) -> Forecast:
        """
        Fetches live data from open-meteo's public coordinate lookup API.
        Applies strict exception handling for network or location errors.
        """
        print(f"[API] Connecting to global weather service for: {location}...")
        
        try:
            # Step 1: Clean the city text name
            city = location.strip().replace(" ", "+")
            
            # Step 2: Request geocoding coordinates for the city name
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            
            with urllib.request.urlopen(geo_url, timeout=10) as response:
                geo_data = json.loads(response.read().decode())
                
            if not geo_data.get("results"):
                raise ValueError(f"Could not find coordinates for location: '{location}'")
                
            # Extract coordinates
            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            
            # Step 3: Fetch the actual weather measurements for those coordinates
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&relative_humidity_2m=true"
            
            with urllib.request.urlopen(weather_url, timeout=10) as response:
                weather_data = json.loads(response.read().decode())
                
            current = weather_data["current_weather"]
            
            # Step 4: Map weather code integers to readable text descriptors
            weather_code = current.get("weathercode", 0)
            condition = "Clear Sky"
            if weather_code in [1, 2, 3]: condition = "Partly Cloudy"
            elif weather_code in [45, 48]: condition = "Foggy"
            elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]: condition = "Rainy"
            elif weather_code in [71, 73, 75, 77, 85, 86]: condition = "Snowy"
            elif weather_code in [95, 96, 99]: condition = "Thunderstorm"

            # Create and return the custom Forecast OOP Object
            return Forecast(
                temperature=float(current["temperature"]),
                condition=condition,
                humidity=int(weather_data.get("current_weather_units", {}).get("relative_humidity_2m", 65)), # fallback default
                wind_speed=float(current["windspeed"])
            )
            
        except urllib.error.URLError:
            print("[Error] Network connection failed. Please check your internet connection.")
            return None
        except ValueError as ve:
            print(f"[Error] {ve}")
            return None
        except Exception as e:
            print(f"[Error] Unexpected system glitch: {e}")
            return None