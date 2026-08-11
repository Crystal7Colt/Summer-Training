import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import streamlit as st

# Load the dataset
df = pd.read_csv("salary_Data.csv")
df = df.dropna(subset=['YearsExperience', 'Salary'])

x = df[['YearsExperience']]
y = df['Salary']

x_train, x_test , y_train , y_test = train_test_split(x, y, test_size=0.2, random_state=42)

lr = LinearRegression()
lr.fit(x_train, y_train)

y_pred = lr.predict(x_test)

# Calculate metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Print metrics to the terminal running the Streamlit server
print("--- Model Evaluation Metrics ---")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R-squared (R2 Score): {r2:.4f}")
print(f"Intercept (c): {lr.intercept_:.4f}")
print(f"Slope/Coefficient (m): {lr.coef_[0]:.4f}")

# Streamlit UI Configuration
st.set_page_config(page_title="Salary Predictor", page_icon="💰", layout="centered")

st.title("Salary Predictor")
st.write("Check your predicted salary using a Linear Regression model based on years of experience.")
st.divider()

exp_input = st.number_input(
    label="Enter Years of Experience:",
    min_value=0.0,
    max_value=50.0,
    value=2.0, 
    step=0.5
)

if st.button("Predict Salary", type="primary"):
    # Using a DataFrame here prevents an sklearn warning about missing feature names
    input_data = pd.DataFrame({'YearsExperience': [exp_input]})
    prediction = lr.predict(input_data)
    
    # Ensure salary doesn't drop below 0 for zero experience
    predicted_salary = max(prediction[0], 0)
    
    st.success("Prediction Successful!")
    st.metric(label="Predicted Salary", value=f"${predicted_salary:,.2f}")
    
    # Conditional UI feedback based on the predicted value
    if predicted_salary >= 100000:
        st.balloons() 
        st.write("Six-figure territory! 🚀")
    elif predicted_salary < 40000:
        st.write("Entry-level phase. Keep building those skills! 💪")