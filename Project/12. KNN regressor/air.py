import streamlit as st
import numpy as np
import pickle

try:
    with open('knn_aqi_model.pkl', 'rb') as file:
        knn = pickle.load(file)

    with open('aqi_scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)
except FileNotFoundError:
    st.error("Error: Pickle files not found. Run the Jupyter Notebook first.")
    st.stop()

st.set_page_config(page_title="AQI Predictor", page_icon="☁️", layout="centered")

st.title("☁️ Air Quality Index (AQI) Predictor")
st.write("Enter the pollutant metrics below to predict the overall Air Quality Index.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    pm25 = st.number_input("PM2.5 Concentration (µg/m³)", min_value=0.0, value=35.0, step=1.0)
    pm10 = st.number_input("PM10 Concentration (µg/m³)", min_value=0.0, value=45.0, step=1.0)

with col2:
    no2 = st.number_input("NO2 Concentration (ppb)", min_value=0.0, value=15.0, step=1.0)
    co = st.number_input("CO Concentration (ppm)", min_value=0.0, value=0.5, step=0.1)

if st.button("Predict AQI", type="primary"):
    # Must match the exact order trained in the notebook: ['pm25', 'pm10', 'no2', 'co']
    input_data = np.array([[pm25, pm10, no2, co]])
    
    input_scaled = scaler.transform(input_data)
    prediction = knn.predict(input_scaled)
    predicted_aqi = int(prediction[0])
    
    st.divider()
    st.success("Prediction Successful!")
    st.metric(label="Predicted AQI (Overall):", value=predicted_aqi)
    
    if predicted_aqi <= 50:
        st.info("Status: Good 🟢")
    elif predicted_aqi <= 100:
        st.warning("Status: Moderate 🟡")
    elif predicted_aqi <= 150:
        st.error("Status: Unhealthy for Sensitive Groups 🟠")
    else:
        st.error("Status: Unhealthy 🔴")