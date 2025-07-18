import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"  

st.title("Urban Project Cost Predictor")

site_area = st.number_input("Site Area", min_value=1)
structure_type = st.selectbox("Structure Type", ["Commercial", "Industrial", "Mixed-use", "Residential"])
water_consumption = st.number_input("Water Consumption", min_value=1)
recycling_rate = st.number_input("Recycling Rate", min_value=1)
utilisation_rate = st.number_input("Utilisation Rate", min_value=1)
air_qality_index = st.number_input("Air Quality Index", min_value=1)
issue_reolution_time = st.number_input("Issue Resolution Time", min_value=1)
resident_count = st.number_input("Resident Count", min_value=1)

#Predict
if st.button("Predict Cost"):
    input_data = {
        "site_area": site_area,
        "structure_type": structure_type,
        "water_consumption": water_consumption,
        "recycling_rate": recycling_rate,
        "utilisation_rate": utilisation_rate,
        "air_qality_index": air_qality_index,
        "issue_reolution_time": issue_reolution_time,
        "resident_count": resident_count
    }

    try:
        response = requests.post(API_URL, json=input_data)

        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ {result}")
        else:
            st.error(f"❌ API Error {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("🚫 Could not connect to FastAPI server. Is it running on port 8000?")
