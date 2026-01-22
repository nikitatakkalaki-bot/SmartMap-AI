import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import google.generativeai as genai

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="SmartMap AI",
    layout="wide",
    page_icon="🎒"
)

# -------------------------------------------------
# GEMINI CONFIG
# -------------------------------------------------
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-pro")
except Exception as e:
    st.error(f"❌ Gemini API Error: {e}")
    st.stop()

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv("clean_travel_data.csv")
    except FileNotFoundError:
        return None

df = load_data()

# -------------------------------------------------
# AI FUNCTION
# -------------------------------------------------
def generate_itinerary(city, country, days, budget, interest):
    prompt = f"""
You are a friendly local travel guide for students.

Create a {days}-day travel itinerary for {city}, {country}.
Total Budget: ${budget}
Student Interests: {interest}

Use this format:

## 📅 Day 1: [Theme]
- 🌅 Morning:
- 🌞 Afternoon:
- 🌙 Evening:

## 💰 Estimated Cost
- 🍽 Food:
- 🚕 Transport:
- 🎟 Activities:
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ AI Error: {e}"

# -------------------------------------------------
# UI HEADER
# -------------------------------------------------
st.title("🎒 SmartMap AI – Student Travel Planner")
st.markdown(
    "✨ *Plan beautiful budget-friendly trips with AI-generated itineraries*"
)

if df is None:
    st.error("❌ clean_travel_data.csv not found!")
    st.stop()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
with st.sidebar:
    st.header("🧭 Trip Planner")

    max_budget = st.slider("💵 Max Daily Budget ($)", 20, 300, 50)

    filtered_data = df[df["Avg_Daily_Cost"] <= max_budget]
    st.success(f"Cities Found: {len(filtered_data)}")

    if filtered_data.empty:
        st.warning("No destinations in this budget.")
        st.stop()

    filtered_data["display"] = (
        filtered_data["city"] + ", " + filtered_data["country"]
    )

    selected = st.selectbox(
        "🌍 Choose Destination",
        filtered_data["display"].unique()
    )

    city, country = selected.split(", ")

    city_info = filtered_data[
        (filtered_data["city"] == city) &
        (filtered_data["country"] == country)
    ].iloc[0]

    days = st.number_input("📆 Trip Duration (Days)", 1, 7, 3)
    interest = st.text_input(
        "🎯 Interests",
        "Street Food, Culture, Photography"
    )

    generate_btn = st.button("🚀 Generate AI Itinerary")

# -------------------------------------------------
# MAIN CONTENT
# -------------------------------------------------
col1, col2 = st.columns([1.3, 1])

# -------- AI RESULT ----------
with col1:
    if generate_btn:
        st.subheader(f"🗺️ Travel Plan for {city}, {country}")
        with st.spinner("✨ AI is creating your travel plan..."):
            plan = generate_itinerary(
                city,
                country,
                days,
                max_budget * days,
                interest
            )
            st.markdown(plan)
    else:
        st.info("👈 Select details and click *Generate*")

# -------- MAP ----------
with col2:
    st.subheader("📍 Location Map")

    m = folium.Map(
        location=[city_info["lat"], city_info["lng"]],
        zoom_start=11
    )

    folium.Marker(
        [city_info["lat"], city_info["lng"]],
        popup=f"{city} (${city_info['Avg_Daily_Cost']}/day)",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

    st_folium(m, width="100%", height=500)

# -------------------------------------------------
# FUTURE SCOPE (PROJECT BEAUTY)
# -------------------------------------------------
st.markdown("---")
st.subheader("🚀 Future Scope of SmartMap AI")

st.markdown("""
- 🏨 Real-time **Hotel & Flight booking integration**
- 🤖 AI-based **budget optimization**
- 👤 **User login system** to save trips
- 🌐 **Multi-language itinerary generation**
- 🌦 Weather-based smart planning
- 👨‍👩‍👧 Group travel planning
- 📱 Android & iOS mobile app
- 🗺 Offline map support
""")
