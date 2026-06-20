import streamlit as st
import json
import os
import re

from weather_client import WeatherClient
from analyzer import ActivityRiskAnalyzer

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Weather Risk & Outdoor Activity Planner",
    page_icon="🌦",
    layout="wide"
)

# ---------------------------
# FILE SETUP
# ---------------------------
if not os.path.exists("history.json"):
    with open("history.json", "w") as f:
        json.dump([], f)

if not os.path.exists("favorites.json"):
    with open("favorites.json", "w") as f:
        json.dump([], f)

# ---------------------------
# TITLE
# ---------------------------
st.title("🌦 Weather Risk & Outdoor Activity Planner")
st.subheader("Weather Safety Dashboard")

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.header("⚙ Control Panel")

location = st.sidebar.text_input("📍 Enter Any City Worldwide", "Lagos")

activity = st.sidebar.selectbox(
    "🏃 Choose Activity",
    ["Football", "Jogging", "Farming", "Picnic", "Travel", "Outdoor Event"]
)

analyze_btn = st.sidebar.button("🚀 Analyze Weather")

# ---------------------------
# QUICK CITIES
# ---------------------------
st.write("🌍 Quick Cities")

col1, col2, col3, col4, col5, col6 = st.columns(6)

for name, col in zip(
    ["London", "Tokyo", "Dubai", "Lagos", "Paris", "Abuja"],
    [col1, col2, col3, col4, col5, col6]
):
    with col:
        if st.button(name):
            location = name

# ---------------------------
# MAIN LOGIC
# ---------------------------
if analyze_btn:

    try:
        clean_location = re.sub(r"[^a-zA-Z\s,]", "", location).strip()

        weather_client = WeatherClient()
        forecast = weather_client.get_weather(clean_location)

        analyzer = ActivityRiskAnalyzer()
        risk = analyzer.analyze(activity, forecast)

        # ---------------------------
        # WEATHER OVERVIEW
        # ---------------------------
        st.subheader("🌤 Weather Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.info(f"📍 {clean_location}")

        with col2:
            st.success(f"🌡 {forecast.temperature}°C")

        with col3:
            st.warning(f"💨 {forecast.wind_speed} km/h")

        with col4:
            st.error(f"🌧 {forecast.precipitation} mm")

        # ---------------------------
        # RISK ANALYSIS
        # ---------------------------
        st.subheader("⚠ Risk Analysis")

        if risk == "Safe":
            st.success("🟢 Risk Level: SAFE")
            advice = "Weather is good for outdoor activities."
        elif risk == "Manageable":
            st.warning("🟡 Risk Level: MANAGEABLE")
            advice = "Be careful outdoors."
        else:
            st.error("🔴 Risk Level: RISKY")
            advice = "Avoid outdoor activity."

        st.write("💡 Advice:", advice)

        # ---------------------------
        # PACKING LIST
        # ---------------------------
        st.subheader("🎒 Packing Checklist")

        items = []

        if activity == "Football":
            items = ["Football boots", "Jersey", "Water bottle", "Shin guards"]
        elif activity == "Jogging":
            items = ["Running shoes", "Water bottle", "Fitness tracker", "Towel"]
        elif activity == "Farming":
            items = ["Hat", "Gloves", "Boots", "Sunscreen", "Water bottle"]
        elif activity == "Picnic":
            items = ["Food", "Water", "Blanket", "Napkins", "Sunscreen"]
        elif activity == "Travel":
            items = ["ID Card", "Phone Charger", "Water", "Passport", "Headphones"]
        elif activity == "Outdoor Event":
            items = ["Umbrella", "Water", "Sunscreen", "Folding Chair", "Sunglasses"]
        else:
            items = ["Water Bottle", "Phone", "Comfortable Clothes"]

        if forecast.precipitation > 0:
            items.append("Raincoat")

        for item in items:
            st.write(f"✔ {item}")

        # ---------------------------
        # GEMINI AI
        # ---------------------------
        st.subheader("🤖 Gemini AI Assistant")

        user_question = st.text_input("Ask AI about weather or safety")

        if user_question:
            try:
                from gemini_client import GeminiClient

                gemini = GeminiClient()

                ai_response = gemini.explain(
                    clean_location,
                    activity,
                    forecast,
                    risk,
                    user_question
                )

                st.info(ai_response)

            except Exception as e:
                st.error(f"Gemini Error: {e}")

        # ---------------------------
        # CHART
        # ---------------------------
        st.subheader("📊 Weather Chart")

        chart_data = {
            "Temperature": [forecast.temperature],
            "Wind Speed": [forecast.wind_speed],
            "Rain": [forecast.precipitation]
        }

        st.bar_chart(chart_data)

        # ---------------------------
        # HISTORY SAVE (FIXED - INSIDE BUTTON)
        # ---------------------------
        try:
            with open("history.json", "r") as f:
                history = json.load(f)

            history.append({
                "location": clean_location,
                "activity": activity,
                "risk": risk
            })

            with open("history.json", "w") as f:
                json.dump(history, f, indent=4)

            st.success("Saved to history ✔")

        except Exception as e:
            st.error(f"History Error: {e}")

    except Exception as e:
        st.error(f"App Error: {e}")

# ---------------------------
# 📜 HISTORY DISPLAY (OUTSIDE BUTTON)
# ---------------------------
with st.expander("📜 History"):
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
        st.json(history)

    except:
        st.info("No history yet.")

# ---------------------------
# ⭐ FAVORITES DISPLAY (OUTSIDE BUTTON)
# ---------------------------
with st.expander("⭐ Favorites"):
    try:
        with open("favorites.json", "r") as f:
            favorites = json.load(f)
        st.json(favorites)

    except:
        st.info("No favorites yet.")