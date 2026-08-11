import streamlit as st
import numpy as np
import pickle

# Load the saved model and scaler
try:
    with open('knn_crop_model.pkl', 'rb') as file:
        knn = pickle.load(file)

    with open('crop_scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)
except FileNotFoundError:
    st.error("Error: Pickle files not found. Please run the Jupyter Notebook first.")
    st.stop()

st.set_page_config(page_title="Crop Recommender", page_icon="🌱", layout="centered")

st.title("🌱 Smart Crop Recommender")
st.write("Enter the soil and environmental metrics below to classify the optimal crop using a KNN algorithm.")
st.divider()

st.subheader("Soil Nutrients")
col1, col2, col3 = st.columns(3)

with col1:
    n_ratio = st.number_input("Nitrogen (N) Ratio:", min_value=0, max_value=150, value=90)
with col2:
    p_ratio = st.number_input("Phosphorous (P) Ratio:", min_value=0, max_value=150, value=42)
with col3:
    k_ratio = st.number_input("Potassium (K) Ratio:", min_value=0, max_value=250, value=43)

st.subheader("Environmental Factors")
col4, col5 = st.columns(2)

with col4:
    temperature = st.number_input("Temperature (°C):", min_value=0.0, max_value=50.0, value=20.8, step=0.1)
    humidity = st.number_input("Humidity (%):", min_value=0.0, max_value=100.0, value=82.0, step=0.5)

with col5:
    ph = st.number_input("Soil pH:", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
    rainfall = st.number_input("Rainfall (mm):", min_value=0.0, max_value=300.0, value=202.9, step=1.0)

if st.button("Recommend Crop", type="primary"):
    # Structure must perfectly match the 7 features trained in the notebook
    input_data = np.array([[n_ratio, p_ratio, k_ratio, temperature, humidity, ph, rainfall]])
    
    # Scale the user input
    input_scaled = scaler.transform(input_data)
    
    # Generate the classification prediction
    prediction = knn.predict(input_scaled)
    recommended_crop = prediction[0].capitalize()
    
    st.divider()
    st.success("Classification Successful!")
    
    # Display the categorical result
    st.markdown(f"### 🌾 Recommended Crop: **{recommended_crop}**")