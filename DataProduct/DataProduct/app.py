from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load your models
with open('models/internet_users.pkl', 'rb') as internet_model_file:
    internet_model = pickle.load(internet_model_file)

with open('models/non_internet_users.pkl', 'rb') as non_internet_model_file:
    non_internet_model = pickle.load(non_internet_model_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    form_data = request.form

    # Prepare data dictionary
    if form_data['Internet Service'] == 'Yes':
        data = {
            'Gender': form_data['Gender'],
            'Age': int(form_data['Age']),
            'Married': form_data['Married'],
            'Number of Dependents': int(form_data['Number of Dependents']),
            'Number of Referrals': int(form_data['Number of Referrals']),
            'Offer': form_data['Offer'],
            'Phone Service': form_data['Phone Service'],
            'Avg Monthly Long Distance Charges': float(form_data['Avg Monthly Long Distance Charges']),
            'Multiple Lines': form_data['Multiple Lines'],
            'Internet Service': form_data['Internet Service'],
            'Internet Type': form_data['Internet Type'],
            'Online Security': form_data['Online Security'],
            'Online Backup': form_data['Online Backup'],
            'Device Protection Plan': form_data['Device Protection Plan'],
            'Premium Tech Support': form_data['Premium Tech Support'],
            'Streaming TV': form_data['Streaming TV'],
            'Streaming Movies': form_data['Streaming Movies'],
            'Streaming Music': form_data['Streaming Music'],
            'Unlimited Data': form_data['Unlimited Data'],
            'Contract': form_data['Contract'],
            'Paperless Billing': form_data['Paperless Billing'],
            'Payment Method': form_data['Payment Method'],
            'Monthly Charge': float(form_data['Monthly Charge']),
            'Total Revenue': float(form_data['Total Revenue']),
            'Region': form_data['Region'],
            'Avg Monthly Charge': float(form_data['Avg Monthly Charge']),
            'Refund Rate': float(form_data['Refund Rate']),
            'Data Efficiency': float(form_data['Data Efficiency']),
        }
    else:
        data = {
            'Gender': form_data['Gender'],
            'Age': int(form_data['Age']),
            'Married': form_data['Married'],
            'Number of Dependents': int(form_data['Number of Dependents']),
            'Number of Referrals': int(form_data['Number of Referrals']),
            'Offer': form_data['Offer'],
            'Phone Service': form_data['Phone Service'],
            'Avg Monthly Long Distance Charges': float(form_data['Avg Monthly Long Distance Charges']),
            'Multiple Lines': form_data['Multiple Lines'],
            'Internet Service': 'No',
            'Internet Type': 'Not Subscribed to Internet',  # Set fixed value
            'Online Security': 'No',  # Disable online services
            'Online Backup': 'No',
            'Device Protection Plan': 'No',  # Disable device protection plan
            'Premium Tech Support': 'No',  # Disable tech support
            'Streaming TV': 'No',  # Disable streaming services
            'Streaming Movies': 'No',
            'Streaming Music': 'No',
            'Unlimited Data': 'No',
            'Contract': form_data['Contract'],
            'Paperless Billing': form_data['Paperless Billing'],
            'Payment Method': form_data['Payment Method'],
            'Monthly Charge': float(form_data['Monthly Charge']),
            'Total Revenue': float(form_data['Total Revenue']),
            'Region': form_data['Region'],
            'Avg Monthly Charge': float(form_data['Avg Monthly Charge']),
            'Refund Rate': float(form_data['Refund Rate']),
            'Data Efficiency': float(form_data['Data Efficiency']),
        }

    # Convert input data to DataFrame for model prediction
    input_data = pd.DataFrame([data])

    # Choose the model based on the Internet Service input
    model = internet_model if form_data['Internet Service'] == 'Yes' else non_internet_model

    # Get prediction and probability
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    # Create a prediction message
    prediction_message = "Customer will churn" if prediction == 1 else "Customer will not churn"
    probability_message = f"Probability of Result: {probability:.2%}"  # Format as percentage

    return render_template('index.html', prediction=prediction_message, probability=probability_message)

if __name__ == '__main__':
    app.run(debug=True)
