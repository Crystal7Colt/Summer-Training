import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import streamlit as st

st.set_page_config(page_title="Insurance Cost Predictor", page_icon="🏥", layout="centered")

@st.cache_resource
def load_and_train():
    try:
        df = pd.read_csv("insurance.csv")
    except FileNotFoundError:
        return None, None
        
    # The dataset uses 'yes'/'no' for smokers. 
    # We convert this to 1/0 so our numerical Regressor can understand it.
    df['smoker'] = df['smoker'].apply(lambda x: 1 if x == 'yes' else 0)
        
    main_features = ['age', 'bmi', 'children', 'smoker']
    
    # Keeping your median imputation logic for robust error handling
    for col in main_features:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].median())
            
    x = df[main_features]
    y = df['charges']
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    
    # Using your exact optimized hyperparameters
    rf = RandomForestRegressor(n_estimators=100, max_depth=12, min_samples_split=2, random_state=42)
    rf.fit(x_train, y_train)
    
    y_pred = rf.predict(x_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print("--- Optimized Random Forest Regressor Metrics ---")
    print(f"MAE: {mae:.4f}")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2 Score: {r2:.4f}")
    
    return rf, x.columns

rf, feature_columns = load_and_train()

if rf is None:
    st.error("Error: 'insurance.csv' not found. Please download it and place it in the same folder.")
    st.stop()

st.title("🏥 Health Insurance Predictor")
st.write("Predict estimated annual medical insurance charges using an optimized Random Forest Regressor.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age:", min_value=18, max_value=100, value=30, step=1)
    bmi = st.number_input("Body Mass Index (BMI):", min_value=10.0, max_value=60.0, value=25.0, step=0.1)

with col2:
    children = st.number_input("Number of Children/Dependents:", min_value=0, max_value=10, value=0, step=1)
    smoker_input = st.selectbox("Smoker?", options=["No", "Yes"])

if st.button("Predict Insurance Cost", type="primary"):
    # Convert UI string selection back to 1 or 0
    smoker_val = 1 if smoker_input == "Yes" else 0
    
    input_data = pd.DataFrame([{
        'age': age, 
        'bmi': bmi, 
        'children': children, 
        'smoker': smoker_val
    }])
    
    input_data = input_data.reindex(columns=feature_columns, fill_value=0)
    prediction = rf.predict(input_data)
    
    st.divider()
    st.success("Prediction Successful!")
    st.metric(label="Estimated Annual Charges:", value=f"${prediction[0]:,.2f}")