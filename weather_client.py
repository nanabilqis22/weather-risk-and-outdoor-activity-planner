class WeatherClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_forecast(self, location: str):
        """
        Task: Fetch weather forecast data from an external API.
        Must apply: Exception handling for network errors & invalid locations.
        """
        print(f"[System] Fetching weather data for: {location}...")
        # TODO: Add API request code here
        pass


class Forecast:
    def __init__(self, temperature: float, condition: str, humidity: int, wind_speed: float):
        self.temperature = temperature
        self.condition = condition
        self.humidity = humidity
        self.wind_speed = wind_speed