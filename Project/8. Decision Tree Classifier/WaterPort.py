import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import streamlit as st

st.set_page_config(page_title="Water Quality Predictor", page_icon="💧", layout="centered")

@st.cache_resource
def load_and_train():
    try:
        df = pd.read_csv("water_potability.csv")
    except FileNotFoundError:
        return None, None
        
    # The water dataset contains some missing values in pH, Sulfate, and Trihalomethanes
    # We fill them with the median of their respective columns
    df.fillna(df.median(), inplace=True)
        
    x = df.drop(columns=['Potability'])
    y = df['Potability']
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    
    # Keeping max_depth to prevent the tree from overfitting
    dt = DecisionTreeClassifier(max_depth=5, random_state=42)
    dt.fit(x_train, y_train)
    
    y_pred = dt.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("--- Decision Tree Metrics ---")
    print(f"Accuracy: {accuracy:.4f}")
    
    return dt, x.columns

dt, feature_columns = load_and_train()

if dt is None:
    st.error("Error: 'water_potability.csv' file not found. Ensure it is saved in the same folder.")
    st.stop()

st.title("💧 Water Potability Predictor")
st.write("Predict if water is safe for human consumption based on its chemical metrics using a Decision Tree Classifier.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    ph = st.number_input("pH Level:", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
    hardness = st.number_input("Hardness (mg/L):", min_value=0.0, max_value=400.0, value=196.0, step=1.0)
    solids = st.number_input("Solids (ppm):", min_value=0.0, max_value=70000.0, value=20000.0, step=100.0)
    chloramines = st.number_input("Chloramines (ppm):", min_value=0.0, max_value=15.0, value=7.1, step=0.1)
    sulfate = st.number_input("Sulfate (mg/L):", min_value=0.0, max_value=500.0, value=333.0, step=1.0)

with col2:
    conductivity = st.number_input("Conductivity (μS/cm):", min_value=0.0, max_value=800.0, value=426.0, step=1.0)
    organic_carbon = st.number_input("Organic Carbon (ppm):", min_value=0.0, max_value=30.0, value=14.2, step=0.1)
    trihalomethanes = st.number_input("Trihalomethanes (μg/L):", min_value=0.0, max_value=130.0, value=66.3, step=0.1)
    turbidity = st.number_input("Turbidity (NTU):", min_value=0.0, max_value=10.0, value=3.9, step=0.1)

if st.button("Predict Potability", type="primary"):
    # Match the exact column names from the dataset
    input_data = pd.DataFrame([{
        'ph': ph,
        'Hardness': hardness,
        'Solids': solids,
        'Chloramines': chloramines,
        'Sulfate': sulfate,
        'Conductivity': conductivity,
        'Organic_carbon': organic_carbon,
        'Trihalomethanes': trihalomethanes,
        'Turbidity': turbidity
    }])
    
    input_data = input_data.reindex(columns=feature_columns, fill_value=0)
    prediction = dt.predict(input_data)
    
    st.divider()
    if prediction[0] == 1:
        st.success("💧 The water is predicted to be POTABLE (Safe to drink).")
    else:
        st.error("⚠️ The water is predicted to be NOT POTABLE (Unsafe).")