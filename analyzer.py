class ActivityRiskAnalyzer:
    
    def analyze(self, activity, forecast):

        temp = forecast.temperature
        wind = forecast.wind_speed
        rain = forecast.precipitation

        # 🌧 rain first (important)
        if rain > 5:
            return "Risky"

        if rain > 0:
            return "Manageable"

        # 🌡 temperature risk
        if temp > 38 or temp < 12:
            return "Risky"

        # 💨 wind risk
        if wind > 25:
            return "Risky"

        return "Safe"