import google.generativeai as genai

API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


class GeminiClient:

    def explain(self, location, activity, forecast, risk):

        prompt = f"""
        You are a weather assistant.

        Location: {location}
        Activity: {activity}

        Weather:
        - Temperature: {forecast.temperature}°C
        - Wind: {forecast.wind_speed} km/h
        - Rain: {forecast.precipitation} mm

        Risk Level: {risk}

        Give a short, simple safety explanation for outdoor activity.
        """

        try:
            response = model.generate_content(prompt)
            return response.text

        except:
            # clean fallback (no API message shown)
            return "AI insight is currently unavailable."