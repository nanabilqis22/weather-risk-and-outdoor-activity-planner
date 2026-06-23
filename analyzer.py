# class ActivityRiskAnalyzer:
 
#     def analyze(self, activity, forecast):

#         temp = forecast.temperature
#         wind = forecast.wind_speed

#         if wind > 25:
#             return "Risky"
#         elif temp > 35:
#             return "Risky"
#         elif temp < 15:
#             return "Manageable"
#         else:
#             return "Safe"
        

class ActivityRiskAnalyzer:

    # Activities that are sensitive to specific conditions
    WIND_SENSITIVE = ["Football", "Outdoor Event", "Picnic"]
    HEAT_SENSITIVE = ["Jogging", "Farming", "Football"]
    COLD_SENSITIVE = ["Jogging", "Farming", "Picnic"]
    RAIN_SENSITIVE = ["Picnic", "Outdoor Event", "Travel"]

    def analyze(self, activity, forecast):

        temp = forecast.temperature
        wind = forecast.wind_speed
        rain = forecast.precipitation

        # --- Base weather rules (apply to everyone) ---

        if temp < 5:
            return "Risky"

        if wind > 25:
            return "Risky"

        if temp > 38:
            return "Risky"

        # --- Activity-specific rules ---

        if activity in self.WIND_SENSITIVE and wind > 18:
            return "Risky"

        if activity in self.HEAT_SENSITIVE and temp > 32:
            return "Risky"

        if activity in self.COLD_SENSITIVE and temp < 15:
            return "Risky"

        if activity in self.RAIN_SENSITIVE and rain > 0:
            return "Manageable"

        if temp < 15 or temp > 32:
            return "Manageable"

        if wind > 15:
            return "Manageable"

        return "Safe"