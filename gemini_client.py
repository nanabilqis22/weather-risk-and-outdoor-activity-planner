import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

try:
    model = genai.GenerativeModel("gemini-3.5-flash")
    response = model.generate_content("Hello")
    st.write("Gemini Model Working")
except Exception as e:
    st.error(f"Model Error: {e}")
model = genai.GenerativeModel("gemini-3.5-flash")


class GeminiClient:

    def explain(
        self,
        location,
        activity,
        forecast,
        risk,
        user_question
    ):

        prompt = f"""
        You are an intelligent weather and safety assistant.

        Location: {location}
        Activity: {activity}

        Weather:
        - Temperature: {forecast.temperature}°C
        - Wind Speed: {forecast.wind_speed} km/h
        - Rainfall: {forecast.precipitation} mm

        Risk Level: {risk}

        User Question:
        {user_question}

        Give a helpful answer based on the weather data above.
        """

        try:
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            return f"Gemini Error: {e}"
