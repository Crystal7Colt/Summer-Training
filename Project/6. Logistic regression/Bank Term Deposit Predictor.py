import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import streamlit as st

st.set_page_config(page_title="Bank Term Deposit Predictor", page_icon="🏦", layout="centered")

@st.cache_resource
def load_and_train():
    try:
        # Bank dataset uses semicolon as separator
        df = pd.read_csv("bank.csv", sep=";")
    except FileNotFoundError:
        return None, None
        
    # Preprocessing
    # Target variable 'y' to binary
    df['y'] = df['y'].map({'yes': 1, 'no': 0})
    
    # Let's drop some complex features to keep UI simple
    cols_to_drop = ['pdays', 'previous', 'poutcome', 'contact', 'day', 'month', 'default']
    df = df.drop(columns=cols_to_drop)
    
    # Get dummies for categorical variables
    categorical_cols = ['job', 'marital', 'education', 'housing', 'loan']
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    
    x = df.drop(columns=['y'])
    y = df['y']
    
    x_train, x_test , y_train , y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    
    lr = LogisticRegression(max_iter=2000, solver='lbfgs')
    lr.fit(x_train, y_train)
    
    return lr, x.columns

lr, feature_columns = load_and_train()

if lr is None:
    st.error("Error: 'bank.csv' file nahi mili. Check karein ki file aapki Python script ke sath sahi folder me rakhi hai.")
    st.stop()

st.title("🏦 Bank Term Deposit Predictor")
st.write("Predict whether a client will subscribe to a term deposit based on their marketing and demographic data.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(label="Age:", min_value=18, max_value=100, value=30)
    job = st.selectbox(label="Job:", options=['unemployed', 'services', 'management', 'blue-collar', 'self-employed', 'technician', 'entrepreneur', 'admin.', 'student', 'housemaid', 'retired', 'unknown'])
    marital = st.selectbox(label="Marital Status:", options=['married', 'single', 'divorced'])
    education = st.selectbox(label="Education:", options=['primary', 'secondary', 'tertiary', 'unknown'])

with col2:
    balance = st.number_input(label="Average Yearly Balance (in €):", min_value=-10000, max_value=100000, value=1500)
    housing = st.selectbox(label="Has Housing Loan?:", options=['yes', 'no'])
    loan = st.selectbox(label="Has Personal Loan?:", options=['yes', 'no'])
    duration = st.number_input(label="Last Contact Duration (seconds):", min_value=0, max_value=5000, value=200)
    campaign = st.number_input(label="Number of Contacts during Campaign:", min_value=1, max_value=50, value=1)

if st.button("Predict Subscription", type="primary"):
    
    input_data = pd.DataFrame([{
        'age': age,
        'balance': balance,
        'duration': duration,
        'campaign': campaign,
        'job': job,
        'marital': marital,
        'education': education,
        'housing': housing,
        'loan': loan
    }])
    
    # Apply get_dummies to user input
    input_encoded = pd.get_dummies(input_data)
    
    # Align columns with training data to ensure all dummy columns are present and ordered correctly
    input_encoded = input_encoded.reindex(columns=feature_columns, fill_value=0)
    
    prediction = lr.predict(input_encoded)
    
    st.divider()
    if prediction[0] == 1:
        st.balloons()
        st.success("The client is predicted to SUBSCRIBE to the term deposit! 🎉")
    else:
        st.error("The client is predicted to NOT SUBSCRIBE to the term deposit. ❌")
