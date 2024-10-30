import streamlit as st
import pickle
import pandas as pd

# Custom CSS and JavaScript for dark theme
st.markdown("""
    <style>
        /* General App Styles */
        .stApp {
            background-color: #2e2e2e;  /* Dark background */
            color: white;  /* White text */
            padding: 20px;
            font-family: 'Arial', sans-serif;
        }

        /* Title Styling */
        h1 {
            color: #ffffff;
            font-weight: bold;
            text-align: center;
            font-size: 2em;
            margin-top: -20px;
            margin-bottom: 20px;
        }

        /* Input Field Styles */
        .stSelectbox, .stNumberInput {
            margin: 10px 0;
            background-color: #444444;  /* Darker input field background */
            color: white;  /* White text for input fields */
            border: 1px solid #555555;  /* Lighter border */
        }

        .stSelectbox label, .stNumberInput label {
            color: #dddddd;  /* Lighter label color */
            font-weight: 600;
            margin-bottom: 5px;
        }

        /* Predict Button */
        button[kind="primary"] {
            background-color: #007bff;
            color: white;
            font-size: 1em;
            font-weight: bold;
            border-radius: 5px;
            padding: 10px 20px;
            margin-top: 20px;
        }

        button[kind="primary"]:hover {
            background-color: #0056b3;
        }

        /* Prediction Output */
        .stMarkdown div p {
            font-size: 1.5em;
            font-weight: bold;
            color: #28a745;  /* Green color for prediction */
            text-align: center;
            margin-top: 20px;
        }
    </style>

    <script>
        // Toggle dark/light theme
        function toggleTheme() {
            var app = document.querySelector('.stApp');
            if (app.style.backgroundColor === 'rgb(46, 46, 46)') {
                app.style.backgroundColor = '#f8f9fa';  // Light background
                app.style.color = 'black';  // Black text
                document.querySelectorAll('.stSelectbox, .stNumberInput').forEach(function(input) {
                    input.style.backgroundColor = 'white';  // Light input background
                    input.style.color = 'black';  // Black text for input fields
                    input.style.border = '1px solid #cccccc';  // Lighter border
                });
                document.querySelectorAll('.stSelectbox label, .stNumberInput label').forEach(function(label) {
                    label.style.color = '#333333';  // Darker label color
                });
            } else {
                app.style.backgroundColor = '#2e2e2e';  // Dark background
                app.style.color = 'white';  // White text
                document.querySelectorAll('.stSelectbox, .stNumberInput').forEach(function(input) {
                    input.style.backgroundColor = '#444444';  // Darker input field background
                    input.style.color = 'white';  // White text for input fields
                    input.style.border = '1px solid #555555';  // Lighter border
                });
                document.querySelectorAll('.stSelectbox label, .stNumberInput label').forEach(function(label) {
                    label.style.color = '#dddddd';  // Lighter label color
                });
            }
        }
    </script>
""", unsafe_allow_html=True)

# Load your trained models
with open('DataProduct/DataProduct/models/internet_users.pkl', 'rb') as f:
    internet_model = pickle.load(f)

with open('DataProduct/DataProduct/models/non_internet_users.pkl', 'rb') as f:
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

# Button to toggle theme
if st.button("Toggle Theme"):
    st.session_state.theme = not st.session_state.get('theme', False)
    st.experimental_rerun()
