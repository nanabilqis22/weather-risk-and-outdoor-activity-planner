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
# UI STYLE
# ---------------------------
st.markdown("""
<style>
body {
    background-color: #0b1220;
}

.title {
    font-size: 34px;
    font-weight: 800;
    text-align: center;
    color: white;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
}

.card {
    background: #111827;
    padding: 18px;
    border-radius: 15px;
    color: white;
    margin-top: 10px;
}

.metric {
    background: #0f172a;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# TITLE (KEEP EXACT NAME)
# ---------------------------
st.markdown('<div class="title">🌦 Weather Risk & Outdoor Activity Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Global Weather Safety Dashboard</div>', unsafe_allow_html=True)

# ---------------------------
# FILES
# ---------------------------
if not os.path.exists("history.json"):
    json.dump([], open("history.json", "w"))

if not os.path.exists("favorites.json"):
    json.dump([], open("favorites.json", "w"))

# ---------------------------
# CONTROL PANEL
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
        # METRICS
        # ---------------------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"<div class='metric'>📍 {clean_location}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div class='metric'>🌡 {forecast.temperature}°C</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='metric'>💨 {forecast.wind_speed} km/h</div>", unsafe_allow_html=True)

        # ---------------------------
        # RISK DISPLAY
        # ---------------------------
        st.subheader("⚠ Risk Analysis")

        if risk == "Safe":
            st.success("🟢 Risk Level: SAFE")
        elif risk == "Manageable":
            st.warning("🟡 Risk Level: MANAGEABLE")
        else:
            st.error("🔴 Risk Level: HIGH RISK")

        # ---------------------------
        # ADVICE
        # ---------------------------
        st.subheader("💡 Safety Advice")

        if risk == "Safe":
            st.write("Weather is good for outdoor activities.")
        elif risk == "Manageable":
            st.write("Be careful, conditions may change.")
        else:
            st.write("Avoid outdoor activity today.")

        # ---------------------------
        # BEST TIME
        # ---------------------------
        st.subheader("⏰ Best Time")

        if risk == "Safe":
            best_time = "Morning or Evening"
        elif risk == "Manageable":
            best_time = "Morning only"
        else:
            best_time = "Not recommended"

        st.write(best_time)

        # ---------------------------
        # PACKING LIST
        # ---------------------------
        st.subheader("🎒 Packing Checklist")

        items = [
            "Water Bottle",
            "Phone",
            "Comfortable Clothes",
            "Cap / Hat"
        ]

        if risk != "Safe":
            items.append("Umbrella / Raincoat")

        for item in items:
            st.write("✔ " + item)

        # ---------------------------
        # CHART
        # ---------------------------
        st.subheader("📊 Weather Chart")

        st.bar_chart({
            "Temperature": [forecast.temperature],
            "Wind Speed": [forecast.wind_speed]
        })

        # ---------------------------
        # HISTORY
        # ---------------------------
        history = json.load(open("history.json"))

        history.append({
            "location": clean_location,
            "activity": activity,
            "risk": risk
        })

        json.dump(history, open("history.json", "w"), indent=4)

        st.success("Saved to history ✔")

    except Exception as e:
        st.error(f"Error: {e}")

# ---------------------------
# FAVORITES
# ---------------------------
st.subheader("⭐ Favorites")

if st.button("Save Favourite"):
    fav = json.load(open("favorites.json"))
    fav.append(location)
    json.dump(fav, open("favorites.json", "w"), indent=4)
    st.success("Saved ✔")

with st.expander("📜 History"):
    st.json(json.load(open("history.json")))

with st.expander("⭐ Favorites"):
    st.json(json.load(open("favorites.json")))