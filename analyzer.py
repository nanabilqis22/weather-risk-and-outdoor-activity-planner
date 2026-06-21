class ActivityRiskAnalyzer:
    
    def analyze(self, activity, forecast):

        temp = forecast.temperature
        wind = forecast.wind_speed

        if wind > 25:
            return "Risky"
        elif temp > 35:
            return "Risky"
        elif temp < 15:
            return "Manageable"
        else:
            return "Safe"
        
        