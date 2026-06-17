import streamlit as st
import json
import os
import re

from weather_client import WeatherClient
from analyzer import ActivityRiskAnalyzer

# ---------------------------
# PAGE CONFIG (DO NOT CHANGE NAME)
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
    json.dump([], open("history.json", "w"))

if not os.path.exists("favorites.json"):
    json.dump([], open("favorites.json", "w"))

# ---------------------------
# UI DESIGN (SaaS STYLE)
# ---------------------------
st.markdown("""
<style>
.title {
    text-align:center;
    font-size:34px;
    font-weight:bold;
    color:#1f77b4;
}

.sub {
    text-align:center;
    color:gray;
    margin-bottom:20px;
}

.card {
    background:#f5f7ff;
    padding:15px;
    border-radius:12px;
    margin:10px 0px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌦 Weather Risk & Outdoor Activity Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Global Weather Safety Dashboard</div>', unsafe_allow_html=True)

# ---------------------------
# INPUTS (CONTROL PANEL STYLE)
# ---------------------------
st.sidebar.header("⚙ Control Panel")

location = st.sidebar.text_input("📍 Enter Any City Worldwide", "London")

activity = st.sidebar.selectbox(
    "🏃 Choose Activity",
    ["Football", "Jogging", "Farming", "Picnic", "Travel", "Outdoor Event"]
)

run = st.sidebar.button("🚀 Analyze Weather")

# ---------------------------
# QUICK CITIES
# ---------------------------
st.markdown("### 🌍 Quick Cities")

cols = st.columns(6)
cities = ["London", "New York", "Tokyo", "Dubai", "Lagos", "Paris"]

for i, city in enumerate(cities):
    with cols[i]:
        if st.button(city):
            location = city

# ---------------------------
# MAIN APP
# ---------------------------
if run and location:

    try:
        clean_location = re.sub(r'[^a-zA-Z\s,]', '', location)

        weather = WeatherClient()
        forecast = weather.get_weather(clean_location)

        analyzer = ActivityRiskAnalyzer()
        risk = analyzer.analyze(activity, forecast)

        # ---------------------------
        # WEATHER DISPLAY
        # ---------------------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"<div class='card'>📍 {clean_location}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div class='card'>🌡 {forecast.temperature}°C</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='card'>💨 {forecast.wind_speed} km/h</div>", unsafe_allow_html=True)

        # ---------------------------
        # RISK
        # ---------------------------
        st.subheader("⚠ Risk Analysis")

        if risk == "Safe":
            st.success("🟢 Risk Level: SAFE")
        elif risk == "Manageable":
            st.warning("🟡 Risk Level: MANAGEABLE")
        else:
            st.error("🔴 RISKY")

        # ---------------------------
        # ADVICE
        # ---------------------------
        if risk == "Safe":
            advice = "Weather is good for outdoor activities."
            best_time = "Morning or Evening"
        elif risk == "Manageable":
            advice = "Be careful outdoors."
            best_time = "Morning only"
        else:
            advice = "Avoid outdoor activity."

        st.subheader("💡 Safety Advice")
        st.write(advice)

        st.subheader("⏰ Best Time")
        st.write(best_time)

        # ---------------------------
        # CHECKLIST
        # ---------------------------
        st.subheader("🎒 Packing Checklist")

        items = ["Water Bottle", "Phone", "Comfortable Clothes", "Cap"]

        if risk != "Safe":
            items.append("Umbrella / Raincoat")

        for i in items:
            st.write("✔", i)

        # ---------------------------
        # 🤖 GEMINI AI (SAFE FALLBACK)
        # ---------------------------
        st.subheader("🤖 Gemini AI Assistant")

        user_question = st.text_input("Ask AI about weather or safety")

        if user_question:
            st.info("🤖 Gemini AI is currently unavailable. Using system recommendations instead.")
            st.write(advice)

        # ---------------------------
        # SAVE HISTORY
        # ---------------------------
        history = json.load(open("history.json"))

        history.append({
            "location": clean_location,
            "activity": activity,
            "risk": risk
        })

        json.dump(history, open("history.json", "w"), indent=4)

        st.success("Saved to history ✔")

        # ---------------------------
        # CHART
        # ---------------------------
        st.subheader("📊 Weather Chart")

        st.bar_chart({
            "Temperature": [forecast.temperature],
            "Wind Speed": [forecast.wind_speed]
        })

    except Exception as e:
        st.error(f"Error: {e}")

# ---------------------------
# FAVORITES
# ---------------------------
st.subheader("⭐ Favorites")

if st.button("Save Favourite"):
    fav = json.load(open("favorites.json"))
    fav.append(location)
    json.dump(fav, open("favorites.json"), "w", indent=4)
    st.success("Saved ✔")

with st.expander("📜 History"):
    st.json(json.load(open("history.json")))

with st.expander("⭐ Favorites"):
    st.json(json.load(open("favorites.json")))