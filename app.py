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
# CUSTOM UI
# ---------------------------
st.markdown("""
<style>
.main-title{
    text-align:center;
    font-size:36px;
    font-weight:bold;
    color:#1f77b4;
}
.sub-title{
    text-align:center;
    color:gray;
    margin-bottom:25px;
}
.card{
    background:#f7f9fc;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🌦 Weather Risk & Outdoor Activity Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Weather Safety Dashboard</div>',
    unsafe_allow_html=True
)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.header("⚙ Control Panel")

location = st.sidebar.text_input(
    "📍 Enter Any City Worldwide",
    "London"
)

activity = st.sidebar.selectbox(
    "🏃 Choose Activity",
    [
        "Football",
        "Jogging",
        "Farming",
        "Picnic",
        "Travel",
        "Outdoor Event"
    ]
)

analyze_btn = st.sidebar.button("🚀 Analyze Weather")

# ---------------------------
# QUICK CITIES
# ---------------------------
st.markdown("### 🌍 Quick Cities")

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    if st.button("London"):
        location = "London"

with c2:
    if st.button("Tokyo"):
        location = "Tokyo"

with c3:
    if st.button("Dubai"):
        location = "Dubai"

with c4:
    if st.button("Lagos"):
        location = "Lagos"

with c5:
    if st.button("Paris"):
        location = "Paris"

with c6:
    if st.button("Abuja"):
        location = "Abuja"

# ---------------------------
# MAIN ANALYSIS
# ---------------------------
if analyze_btn:

    try:
        clean_location = re.sub(
            r"[^a-zA-Z\s,]",
            "",
            location
        ).strip()

        weather = WeatherClient()
        forecast = weather.get_weather(clean_location)

        analyzer = ActivityRiskAnalyzer()
        risk = analyzer.analyze(activity, forecast)

        # ---------------------------
        # WEATHER OVERVIEW
        # ---------------------------
        st.subheader("🌤 Weather Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info(f"📍 {clean_location}")

        with col2:
            st.success(f"🌡 {forecast.temperature}°C")

        with col3:
            st.warning(f"💨 {forecast.wind_speed} km/h")

        # ---------------------------
        # RISK ANALYSIS
        # ---------------------------
        st.subheader("⚠ Risk Analysis")

        if risk == "Safe":
            st.success("🟢 Risk Level: SAFE")
            advice = "Weather is good for outdoor activities."
            best_time = "Morning or Evening"

        elif risk == "Manageable":
            st.warning("🟡 Risk Level: MANAGEABLE")
            advice = "Be careful outdoors."
            best_time = "Morning Only"

        else:
            st.error("🔴 Risk Level: RISKY")
            advice = "Avoid outdoor activity."
            best_time = "Not Recommended"

        # ---------------------------
        # ADVICE
        # ---------------------------
        st.subheader("💡 Safety Advice")
        st.write(advice)

        # ---------------------------
        # BEST TIME
        # ---------------------------
        st.subheader("⏰ Best Time")
        st.write(best_time)

        # ---------------------------
        # CHECKLIST
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
            st.write("✔", item)

        # ---------------------------
        # GEMINI PLACEHOLDER
        # ---------------------------
        st.subheader("🤖 Gemini AI Assistant")

        user_question = st.text_input(
            "Ask AI about weather or safety"
        )

        if user_question:
            st.info(
                "🤖 Gemini AI is currently unavailable. Using system recommendations."
            )
            st.write(advice)

        # ---------------------------
        # SAVE HISTORY
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

        # ---------------------------
        # CHART
        # ---------------------------
        st.subheader("📊 Weather Chart")

        chart_data = {
            "Temperature": [forecast.temperature],
            "Wind Speed": [forecast.wind_speed]
        }

        st.bar_chart(chart_data)

    except Exception as e:
        st.error(f"Error: {e}")

# ---------------------------
# FAVORITES
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
# HISTORY
# ---------------------------
with st.expander("📜 History"):
    with open("history.json", "r") as f:
        st.json(json.load(f))

# ---------------------------
# FAVORITES LIST
# ---------------------------
with st.expander("⭐ Favorites"):
    with open("favorites.json", "r") as f:
        st.json(json.load(f))