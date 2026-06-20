class ActivityRiskAnalyzer:

    def analyze(self, activity, forecast):

        temp = forecast.temperature
        wind = forecast.wind_speed
        rain = forecast.precipitation

        activity = activity.lower()

        # FOOTBALL
        if activity == "football":

            if rain >= 5:
                return "Avoid"

            if rain > 0:
                return "Risky"

            if wind > 30:
                return "Risky"

            return "Safe"

        # JOGGING
        elif activity == "jogging":

            if rain > 0:
                return "Risky"

            if temp > 35:
                return "Risky"

            if temp < 10:
                return "Risky"

            return "Safe"

        # PICNIC
        elif activity == "picnic":

            if rain > 0:
                return "Avoid"

            if wind > 25:
                return "Risky"

            return "Safe"

        # FARMING
        elif activity == "farming":

            if rain >= 2:
                return "Safe"

            if rain > 0:
                return "Manageable"

            return "Irrigation Needed"

        # TRAVELLING
        elif activity == "travelling":

            if rain >= 10:
                return "Avoid"

            if rain > 0:
                return "Risky"

            if wind > 35:
                return "Risky"

            return "Safe"

        # OUTDOOR EVENT
        elif activity == "outdoor event":

            if rain >= 5:
                return "Avoid"

            if rain > 0:
                return "Risky"

            if wind > 25:
                return "Risky"

            return "Safe"

        # DEFAULT
        else:

            if rain >= 5:
                return "Avoid"

            if rain > 0:
                return "Risky"

            if temp > 38 or temp < 12:
                return "Risky"

            if wind > 25:
                return "Risky"

            return "Safe"
