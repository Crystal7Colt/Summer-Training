import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import streamlit as st
from datetime import date

st.set_page_config(page_title="Used Car Price Predictor", page_icon="🚗", layout="centered")

@st.cache_resource
def load_and_train():
    try:
        df = pd.read_csv("car_data.csv")
    except FileNotFoundError:
        return None, None
        
    current_year = date.today().year
    df['CarAge'] = current_year - df['Year']
    
    # ADDED Present_Price to the features so the model knows the baseline value
    x = df[['CarAge', 'Kms_Driven', 'Present_Price']]
    y = df['Selling_Price']
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    
    dtr = DecisionTreeRegressor(max_depth=5, random_state=42)
    dtr.fit(x_train, y_train)
    
    return dtr, x.columns

dtr, feature_columns = load_and_train()

if dtr is None:
    st.error("Error: 'car_data.csv' not found. Please ensure it is in the same folder.")
    st.stop()

st.title("🚗 Used Car Price Predictor")
st.write("Predict the estimated resale value using Age, Distance, and Original Price.")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    age_input = st.number_input("Car Age (Years):", min_value=0, max_value=30, value=5, step=1)

with col2:
    kms_input = st.number_input("Kilometers Driven:", min_value=0, max_value=500000, value=50000, step=1000)

with col3:
    # Adding the original price input in Lakhs
    present_price_input = st.number_input("Original Price (in Lakhs):", min_value=0.0, max_value=100.0, value=5.5, step=0.5)

if st.button("Predict Resale Value", type="primary"):
    # Ensure inputs exactly match the 3 features we trained on
    input_data = pd.DataFrame([{
        'CarAge': age_input,
        'Kms_Driven': kms_input,
        'Present_Price': present_price_input
    }])
    
    input_data = input_data.reindex(columns=feature_columns, fill_value=0)
    prediction = dtr.predict(input_data)
    
    st.divider()
    st.success("Prediction Successful!")
    
    actual_price = prediction[0] * 100000
    st.metric(label="Estimated Resale Value:", value=f"₹{actual_price:,.2f}")