import streamlit as st
import json
import os
import re

from weather_client import WeatherClient
from analyzer import ActivityRiskAnalyzer

# PAGE CONFIG
st.set_page_config(
    page_title="Weather Risk & Outdoor Activity Planner",
    page_icon="🌦",
    layout="wide"
)

# SESSION STATE INITIALIZATION
if "forecast" not in st.session_state:
    st.session_state.forecast = None

if "risk" not in st.session_state:
    st.session_state.risk = None

if "location" not in st.session_state:
    st.session_state.location = None

if "activity" not in st.session_state:
    st.session_state.activity = None

# FILE SETUP
if not os.path.exists("history.json"):
    with open("history.json", "w") as f:
        json.dump([], f)

if not os.path.exists("favorites.json"):
    with open("favorites.json", "w") as f:
        json.dump([], f)

# TITLE
st.title("🌦 Weather Risk & Outdoor Activity Planner")
st.subheader("Weather Safety Dashboard")

# SIDEBAR
st.sidebar.header("⚙ Control Panel")

# Use a default state hook to tie quick-city selections smoothly
default_city = "Lagos"
location = st.sidebar.text_input("📍 Enter Any City Worldwide", default_city)

activity = st.sidebar.selectbox(
    "🏃 Choose Activity",
    ["Football", "Jogging", "Farming", "Picnic", "Travel", "Outdoor Event"]
)

analyze_btn = st.sidebar.button("🚀 Analyze Weather")

# QUICK CITIES
st.write("🌍 Quick Cities")

col1, col2, col3, col4, col5, col6 = st.columns(6)

for name, col in zip(
    ["London", "Tokyo", "Dubai", "Lagos", "Paris", "Abuja"],
    [col1, col2, col3, col4, col5, col6]
):
    with col:
        if st.button(name):
            location = name

# MAIN LOGIC (WEATHER ANALYSIS)
if analyze_btn:
    try:
        clean_location = re.sub(r"[^a-zA-Z\s,]", "", location).strip()

        weather_client = WeatherClient()
        forecast = weather_client.get_weather(clean_location)

        analyzer = ActivityRiskAnalyzer()
        risk = analyzer.analyze(activity, forecast)

        # Save results into Session State so they survive text input reruns
        st.session_state.forecast = forecast
        st.session_state.risk = risk
        st.session_state.location = clean_location
        st.session_state.activity = activity

        # Save to history file directly during the trigger event
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

        except Exception as e:
            st.error(f"History Save Error: {e}")

    except Exception as e:
        st.error(f"App Error: {e}")

# DISPLAY RESULTS (IF STATE EXISTS)
if st.session_state.forecast:
    # Shortcuts for easier code management below
    f_state = st.session_state.forecast
    r_state = st.session_state.risk
    loc_state = st.session_state.location
    act_state = st.session_state.activity

    # Weather Overview
    st.subheader("🌤 Weather Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info(f"📍 {loc_state}")
    with col2:
        st.success(f"🌡 {f_state.temperature}°C")
    with col3:
        st.warning(f"💨 {f_state.wind_speed} km/h")
    with col4:
        st.error(f"🌧 {f_state.precipitation} mm")

    # RISK ANALYSIS
    st.subheader("⚠ Risk Analysis")

    if r_state == "Safe":
        st.success("🟢 Risk Level: SAFE")
        advice = "Weather is good for outdoor activities."
    elif r_state == "Manageable":
        st.warning("🟡 Risk Level: MANAGEABLE")
        advice = "Be careful outdoors."
    else:
        st.error("🔴 Risk Level: RISKY")
        advice = "Avoid outdoor activity."

    st.write("💡 Advice:", advice)

    # PACKING LIST
    st.subheader("🎒 Packing Checklist")

    items = []
    if act_state == "Football":
        items = ["Football boots", "Jersey", "Water bottle", "Shin guards"]
    elif act_state == "Jogging":
        items = ["Running shoes", "Water bottle", "Fitness tracker", "Towel"]
    elif act_state == "Farming":
        items = ["Hat", "Gloves", "Boots", "Sunscreen", "Water bottle"]
    elif act_state == "Picnic":
        items = ["Food", "Water", "Blanket", "Napkins", "Sunscreen"]
    elif act_state == "Travel":
        items = ["ID Card", "Phone Charger", "Water", "Passport", "Headphones"]
    elif act_state == "Outdoor Event":
        items = ["Umbrella", "Water", "Sunscreen", "Folding Chair", "Sunglasses"]
    else:
        items = ["Water Bottle", "Phone", "Comfortable Clothes"]

    if f_state.precipitation > 0:
        items.append("Raincoat")

    for item in items:
        st.write(f"✔ {item}")

    # CHART
    st.subheader("📊 Weather Chart")

    chart_data = {
        "Temperature": [f_state.temperature],
        "Wind Speed": [f_state.wind_speed],
        "Rain": [f_state.precipitation]
    }
    st.bar_chart(chart_data)

    # GEMINI AI ASSISTANT (PERSISTENT OUTSIDE BUTTON CLICK)
    st.markdown("---")
    st.subheader("🤖 Gemini AI Assistant")

    user_question = st.text_input("Ask AI about weather or safety", key="gemini_input_box")

    if st.button("Ask Gemini"):
        if user_question.strip() != "":
            with st.spinner("Consulting Gemini..."):
                try:
                    from gemini_client import GeminiClient

                    gemini = GeminiClient()
                    ai_response = gemini.explain(
                        loc_state,
                        act_state,
                        f_state,
                        r_state,
                        user_question
                    )
                    st.info(ai_response)

                except Exception as e:
                    st.error(f"Gemini UI Error: {e}")
        else:
            st.warning("Please enter a question first!")
            
# 📜 HISTORY DISPLAY
with st.expander("📜 History"):
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
        st.json(history)
    except:
        st.info("No history yet.")

# ⭐ FAVORITES DISPLAY
with st.expander("⭐ Favorites"):
    try:
        with open("favorites.json", "r") as f:
            favorites = json.load(f)
        st.json(favorites)
    except:
        st.info("No favorites yet.")
