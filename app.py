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

with col1:
    if st.button("London"):
        location = "London"

with col2:
    if st.button("Tokyo"):
        location = "Tokyo"

with col3:
    if st.button("Dubai"):
        location = "Dubai"

with col4:
    if st.button("Lagos"):
        location = "Lagos"

with col5:
    if st.button("Paris"):
        location = "Paris"

with col6:
    if st.button("Abuja"):
        location = "Abuja"

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

        st.write("🌧 Rain Status:", forecast.precipitation)

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
        # 🎒 PACKING CHECKLIST
        # ---------------------------
        st.subheader("🎒 Packing Checklist")

        if activity == "Football":
            items = [
                "Football boots",
                "Jersey",
                "Water bottle",
                "Shin guards"
            ]

        elif activity == "Jogging":
            items = [
                "Running shoes",
                "Water bottle",
                "Fitness tracker",
                "Towel"
            ]

        elif activity == "Farming":
            items = [
                "Hat",
                "Gloves",
                "Boots",
                "Sunscreen",
                "Water bottle"
            ]

        elif activity == "Picnic":
            items = [
                "Food",
                "Water",
                "Blanket",
                "Napkins",
                "Sunscreen"
            ]

        elif activity == "Travel":
            items = [
                "ID Card",
                "Phone Charger",
                "Water",
                "Passport",
                "Headphones"
            ]

        elif activity == "Outdoor Event":
            items = [
                "Umbrella",
                "Water",
                "Sunscreen",
                "Folding Chair",
                "Sunglasses"
            ]

        else:
            items = [
                "Water Bottle",
                "Phone",
                "Comfortable Clothes"
            ]

        if forecast.precipitation > 0:
            items.append("Raincoat")

        for item in items:
            st.write(f"✔ {item}")

        # ---------------------------
        # 🤖 GEMINI AI ASSISTANT
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
                    risk
                )

                st.info(ai_response)

            except Exception:
                st.warning("🤖 AI Assistant is currently unavailable")

        # ---------------------------
        # 📊 WEATHER CHART
        # ---------------------------
        st.subheader("📊 Weather Chart")

        chart_data = {
            "Temperature": [forecast.temperature],
            "Wind Speed": [forecast.wind_speed],
            "Rain": [forecast.precipitation]
        }

        st.bar_chart(chart_data)

        # ---------------------------
        # HISTORY
        # ---------------------------
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
        st.error(f"Error: {e}")

# ---------------------------
# ⭐ FAVORITES
# ---------------------------
st.subheader("⭐ Favorites")

if st.button("Save Favourite"):

    with open("favorites.json", "r") as f:
        fav = json.load(f)

    fav.append(location)

    with open("favorites.json", "w") as f:
        json.dump(fav, f, indent=4)

    st.success("Saved ✔")

# ---------------------------
# 📜 HISTORY DISPLAY
# ---------------------------
with st.expander("📜 History"):
    with open("history.json", "r") as f:
        st.json(json.load(f))

# ---------------------------
# ⭐ FAVORITES DISPLAY
# ---------------------------
with st.expander("⭐ Favorites"):
    with open("favorites.json", "r") as f:
        st.json(json.load(f))