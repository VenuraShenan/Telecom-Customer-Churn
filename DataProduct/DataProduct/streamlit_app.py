import streamlit as st
import pickle
import pandas as pd

# Load your trained models
with open('DataProduct/DataProduct/models/internet_users.pkl', 'rb') as f:
    internet_model = pickle.load(f)

with open('DataProduct/DataProduct/models/internet_users.pkl', 'rb') as f:
    non_internet_model = pickle.load(f)

# Function to predict customer churn
def predict_churn(data, model):
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    probability = model.predict_proba(df)  # Get the class probabilities
    return prediction[0], probability[0]  # Return both prediction and probabilities

# Streamlit app
st.title("Customer Churn Prediction")

# Input fields
gender = st.selectbox("Gender", ["Female", "Male"])
age = st.number_input("Age", min_value=0)
married = st.selectbox("Married", ["Yes", "No"])
number_of_dependents = st.number_input("Number of Dependents", min_value=0)
number_of_referrals = st.number_input("Number of Referrals", min_value=0)
offer = st.selectbox("Offer", ["Declined", "Offer E", "Offer D", "Offer A", "Offer B", "Offer C"])

# Internet Service selection
internet_service = st.selectbox("Internet Service", ["Yes", "No"])

# Phone Service input
phone_service = st.selectbox("Phone Service", ["Yes", "No"])

avg_monthly_long_distance_charges = st.number_input("Avg Monthly Long Distance Charges", min_value=0.0)
multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "Not Subscribed to phone"])

# Initialize internet-related fields
internet_type = "Not Subscribed to Internet"
online_security = "No"
online_backup = "No"
device_protection_plan = "No"
premium_tech_support = "No"
streaming_tv = "No"
streaming_movies = "No"
streaming_music = "No"
unlimited_data = "No"

if internet_service == "Yes":
    internet_type = st.selectbox("Internet Type", ["Cable", "Fiber Optic", "DSL"])
    online_security = st.selectbox("Online Security", ["No", "Yes"])
    online_backup = st.selectbox("Online Backup", ["Yes", "No"])
    device_protection_plan = st.selectbox("Device Protection Plan", ["No", "Yes"])
    premium_tech_support = st.selectbox("Premium Tech Support", ["Yes", "No"])
    streaming_tv = st.selectbox("Streaming TV", ["Yes", "No"])
    streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes"])
    streaming_music = st.selectbox("Streaming Music", ["No", "Yes"])
    unlimited_data = st.selectbox("Unlimited Data", ["Yes", "No"])

# Other inputs
contract = st.selectbox("Contract", ["One Year", "Month-to-Month", "Two Year"])
paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
payment_method = st.selectbox("Payment Method", ["Credit Card", "Bank Withdrawal", "Mailed Check"])
monthly_charge = st.number_input("Monthly Charge", min_value=0.0)
total_revenue = st.number_input("Total Revenue", min_value=0.0)
region = st.selectbox("Region", ["Central Coast", "Los Angeles Region", "Orange County", "Bay Area", "Other", 
                                   "Napa Valley", "Silicon Valley", "North Coast", "Northern California", 
                                   "San Diego County", "Sacramento Valley", "Inland Empire", "High Sierra"])
avg_monthly_charge = st.number_input("Avg Monthly Charge", min_value=0.0)
refund_rate = st.number_input("Refund Rate", min_value=0.0)
data_efficiency = st.number_input("Data Efficiency", min_value=0.0)

# Prepare data for prediction
input_data = {
    "Gender": gender,
    "Age": age,
    "Married": married,
    "Number of Dependents": number_of_dependents,
    "Number of Referrals": number_of_referrals,
    "Offer": offer,
    "Phone Service": phone_service,
    "Avg Monthly Long Distance Charges": avg_monthly_long_distance_charges,
    "Multiple Lines": multiple_lines,
    "Internet Service": internet_service,
    "Internet Type": internet_type,
    "Online Security": online_security,
    "Online Backup": online_backup,
    "Device Protection Plan": device_protection_plan,
    "Premium Tech Support": premium_tech_support,
    "Streaming TV": streaming_tv,
    "Streaming Movies": streaming_movies,
    "Streaming Music": streaming_music,
    "Unlimited Data": unlimited_data,
    "Contract": contract,
    "Paperless Billing": paperless_billing,
    "Payment Method": payment_method,
    "Monthly Charge": monthly_charge,
    "Total Revenue": total_revenue,
    "Region": region,
    "Avg Monthly Charge": avg_monthly_charge,
    "Refund Rate": refund_rate,
    "Data Efficiency": data_efficiency,
}

# Predict button
if st.button("Predict"):
    if internet_service == "Yes":
        prediction, _ = predict_churn(input_data, internet_model)
    else:
        prediction, _ = predict_churn(input_data, non_internet_model)

    # Display the prediction result only
    st.write("Prediction:", "Churned" if prediction == 1 else "Not Churned")
