import streamlit as st
import numpy as np
import pickle

# Load the saved model and scaler
try:
    with open('kmeans_model.pkl', 'rb') as file:
        kmeans = pickle.load(file)

    with open('kmeans_scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)
except FileNotFoundError:
    st.error("Error: Pickle files not found. Please run the Jupyter Notebook first.")
    st.stop()

st.set_page_config(page_title="Customer Segmentation", page_icon="🛍️", layout="centered")

st.title("🛍️ Smart Customer Segmentation")
st.write("Enter customer financial metrics to assign them to a marketing segment using K-Means Clustering.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    income = st.number_input("Annual Income (in $1,000s):", min_value=10.0, max_value=200.0, value=50.0, step=1.0)

with col2:
    spending = st.number_input("Spending Score (1-100):", min_value=1, max_value=100, value=50, step=1)

if st.button("Segment Customer", type="primary"):
    # Format the input data
    input_data = np.array([[income, spending]])
    
    # Scale the user input using the exact same logic from the training data
    input_scaled = scaler.transform(input_data)
    
    # Predict the cluster (will output a number between 0 and 4)
    cluster_prediction = kmeans.predict(input_scaled)[0]
    
    st.divider()
    st.success("Segmentation Successful!")
    st.metric(label="Assigned Customer Group:", value=f"Cluster {cluster_prediction}")
    
    # Provide business context to the clusters based on standard Mall Customer distributions
    if cluster_prediction == 0:
        st.info("**Profile:** Moderate Income / Moderate Spenders. \n\n*Action:* Standard marketing promotions.")
    elif cluster_prediction == 1:
        st.warning("**Profile:** High Income / Low Spenders. \n\n*Action:* Needs targeted campaigns to encourage spending.")
    elif cluster_prediction == 2:
        st.error("**Profile:** Low Income / Low Spenders. \n\n*Action:* Focus on essential, budget-friendly items.")
    elif cluster_prediction == 3:
        st.success("**Profile:** Low Income / High Spenders. \n\n*Action:* High engagement, but monitor for responsible marketing.")
    elif cluster_prediction == 4:
        st.balloons()
        st.success("**Profile:** High Income / High Spenders. \n\n*Action:* Target with premium products and loyalty programs!")