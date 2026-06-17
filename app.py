import streamlit as st
import json
import os
import re
import google.generativeai as genai

from weather_client import WeatherClient
from analyzer import ActivityRiskAnalyzer

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Weather Risk Planner",
    page_icon="🌦",
    layout="centered"
)

# ---------------------------
# GEMINI SETUP
# ---------------------------
AI_AVAILABLE = False

try:
    genai.configure(api_key=st.secrets[""])
    model = genai.GenerativeModel("gemini-1.5-flash")
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

# ---------------------------
# FILE SETUP
# ---------------------------
os.makedirs(".", exist_ok=True)

if not os.path.exists("history.json"):
    json.dump([], open("history.json", "w"))

if not os.path.exists("favorites.json"):
    json.dump([], open("favorites.json", "w"))

# ---------------------------
# UI DESIGN
# ---------------------------
st.markdown("""
<style>
.title {
    text-align:center;
    font-size:32px;
    font-weight:bold;
    color:#1f77b4;
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

# ---------------------------
# INPUTS
# ---------------------------
location = st.text_input("📍 Enter Location")

activity = st.selectbox(
    "🏃 Choose Activity",
    ["Football", "Jogging", "Farming", "Picnic", "Travel", "Event"]
)

# ---------------------------
# MAIN BUTTON
# ---------------------------
if st.button("Analyze Weather"):

    if location.strip() == "":
        st.error("Please enter a location")
        st.stop()

    try:
        # CLEAN LOCATION (REGEX)
        clean_location = re.sub(r'[^a-zA-Z\s]', '', location)

        # GET WEATHER
        weather = WeatherClient()
        forecast = weather.get_weather(clean_location)

        # RISK ANALYSIS
        analyzer = ActivityRiskAnalyzer()
        risk = analyzer.analyze(activity, forecast)

        # ---------------------------
        # WEATHER DISPLAY
        # ---------------------------
        st.subheader("🌤 Weather Overview")

        st.markdown(f"""
        <div class="card">
        📍 <b>{clean_location}</b><br>
        🌡 Temperature: {forecast.temperature}°C<br>
        💨 Wind Speed: {forecast.wind_speed} km/h
        </div>
        """, unsafe_allow_html=True)

        # ---------------------------
        # RISK
        # ---------------------------
        st.subheader("⚠ Risk Analysis")

        st.markdown(f"""
        <div class="card">
        Risk Level: <b>{risk}</b>
        </div>
        """, unsafe_allow_html=True)

        # ---------------------------
        # SAFETY ADVICE
        # ---------------------------
        st.subheader("💡 Safety Advice")

        if risk == "Safe":
            advice = "Weather conditions are suitable for outdoor activity."
            best_time = "Morning or Evening"
        elif risk == "Manageable":
            advice = "Be cautious and avoid long exposure outdoors."
            best_time = "Morning only"
        else:
            advice = "Avoid outdoor activity due to unsafe weather conditions."
            best_time = "Not recommended"

        st.write(advice)

        # ---------------------------
        # BEST TIME
        # ---------------------------
        st.subheader("⏰ Best Time")
        st.write(best_time)

        # ---------------------------
        # PACKING CHECKLIST
        # ---------------------------
        st.subheader("🎒 Packing Checklist")

        items = [
            "Water bottle",
            "Phone",
            "Comfortable clothing",
            "Cap/Hat"
        ]

        if risk != "Safe":
            items.append("Umbrella / Raincoat")

        for item in items:
            st.write("✔", item)

        # ---------------------------
        # GEMINI AI SECTION
        # ---------------------------
        st.subheader("🤖 AI Insight (Gemini)")

        prompt = f"""
        You are a weather safety assistant.

        Location: {clean_location}
        Activity: {activity}
        Temperature: {forecast.temperature}
        Wind Speed: {forecast.wind_speed}
        Risk Level: {risk}

        Give:
        - Safety advice
        - Best time of day
        - Simple explanation
        Keep it short and clear.
        """

        if AI_AVAILABLE:
            try:
                response = model.generate_content(prompt)
                st.success("AI Analysis")
                st.write(response.text)

            except:
                st.warning("🤖 AI temporarily unavailable. Using system-based recommendations.")
                st.write(advice)
        else:
            st.info("Gemini not configured on this system.")

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
        # WEATHER CHART (FIXED)
        # ---------------------------
        st.subheader("📊 Weather Chart")

        st.line_chart({
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
    json.dump(fav, open("favorites.json", "w"), indent=4)
    st.success("Saved ✔")

# ---------------------------
# VIEW DATA
# ---------------------------
with st.expander("📜 History"):
    st.json(json.load(open("history.json")))

with st.expander("⭐ Favorites"):
    st.json(json.load(open("favorites.json")))