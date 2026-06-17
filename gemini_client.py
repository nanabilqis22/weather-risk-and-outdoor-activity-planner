import google.generativeai as genai

class GeminiClient:

    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def get_response(self, location, activity, forecast, risk, question):
        prompt = f"""
You are a weather safety assistant.

Location: {location}
Activity: {activity}
Temperature: {forecast.temperature}
Wind Speed: {forecast.wind_speed}
Risk Level: {risk}

User Question: {question}

Give:
- Safety advice
- Best time of day
- Clear explanation
"""

        response = self.model.generate_content(prompt)
        return response.text