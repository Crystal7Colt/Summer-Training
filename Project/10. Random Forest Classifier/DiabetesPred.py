import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import streamlit as st

st.set_page_config(page_title="Diabetes Risk Predictor", page_icon="🩸", layout="centered")

@st.cache_resource
def load_and_train():
    try:
        df = pd.read_csv("diabetes.csv")
    except FileNotFoundError:
        return None, None
        
    df = df.dropna()
    
    if len(df) <= 5:
        return "INSUFFICIENT_DATA", None
        
    # Selected 6 key features to match the dual-column UI layout
    main_features = ['Glucose', 'BloodPressure', 'BMI', 'Insulin', 'DiabetesPedigreeFunction', 'Age']
    
    for col in main_features:
        if col not in df.columns:
            return "MISSING_COLUMNS", None

    x = df[main_features]
    y = df['Outcome']
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    
    # Random Forest is excellent for this dataset due to non-linear relationships
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(x_train, y_train)
    
    y_pred = rf.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("--- Random Forest Classifier Metrics ---")
    print(f"Accuracy: {accuracy:.4f}")
    
    return rf, x.columns

rf, feature_columns = load_and_train()

if rf is None:
    st.error("Error: 'diabetes.csv' file not found. Please place it in the same directory.")
    st.stop()
elif rf == "INSUFFICIENT_DATA":
    st.error("Error: The dataset has too few rows to train the model safely.")
    st.stop()
elif rf == "MISSING_COLUMNS":
    st.error("Error: Required medical columns are missing from the dataset.")
    st.stop()

st.title("🩸 Diabetes Risk Predictor")
st.write("Predict the likelihood of diabetes based on key health metrics using a Random Forest Classifier.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    glucose = st.number_input("Glucose Level:", min_value=0, max_value=250, value=120)
    bp = st.number_input("Blood Pressure (mm Hg):", min_value=0, max_value=150, value=70)
    bmi = st.number_input("BMI (Body Mass Index):", min_value=0.0, max_value=70.0, value=25.5, step=0.1)

with col2:
    insulin = st.number_input("Insulin Level (mu U/ml):", min_value=0, max_value=900, value=79)
    dpf = st.number_input("Diabetes Pedigree Function:", min_value=0.0, max_value=3.0, value=0.5, step=0.01)
    age = st.number_input("Age:", min_value=1, max_value=120, value=33)

if st.button("Predict Health Status", type="primary"):
    # Ensure inputs match the features we trained on exactly
    input_data = pd.DataFrame([{
        'Glucose': glucose,
        'BloodPressure': bp,
        'BMI': bmi,
        'Insulin': insulin,
        'DiabetesPedigreeFunction': dpf,
        'Age': age
    }])
    
    input_data = input_data.reindex(columns=feature_columns, fill_value=0)
    prediction = rf.predict(input_data)
    
    st.divider()
    if prediction[0] == 1:
        st.error("Warning: High risk of diabetes detected based on the provided metrics.")
    else:
        st.success("Good news: Low risk of diabetes detected.")