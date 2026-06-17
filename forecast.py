class Forecast:
    def __init__(self, temperature, wind_speed, precipitation):
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.precipitation = precipitation

    def to_dict(self):
        return {
            "temperature": self.temperature,
            "wind_speed": self.wind_speed,
            "precipitation": self.precipitation
        }