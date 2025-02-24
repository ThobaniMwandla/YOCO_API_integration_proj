import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Yoco API details
YOCO_SECRET_KEY = os.getenv("YOCO_SECRET_KEY")
YOCO_PAYMENT_ENDPOINT = "https://online.yoco.com/v1/charges/"
TRANSACTIONS_API_URL = "https://online.yoco.com/v1/transactions"

def create_charge(amount, token):
    headers = {
        'X-Auth-Secret-Key': YOCO_SECRET_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'amountInCents': amount,
        'currency': 'ZAR',
        'token': token
    }
    response = requests.post(YOCO_PAYMENT_ENDPOINT, headers=headers, json=data)
    return response.json()

def fetch_transactions():
    headers = {
        'X-Auth-Secret-Key': YOCO_SECRET_KEY
    }
    response = requests.get(TRANSACTIONS_API_URL, headers=headers)
    transactions = response.json().get('data', [])
    return transactions

@app.route('/', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        data = request.get_json()
        print("Received data:", data)  # Log incoming JSON data
        amount = int(data['amount']) * 100  # Correct variable name
        token = data['token']
        charge_response = create_charge(amount, token)
        return jsonify(charge_response)

    transactions = fetch_transactions()
    return render_template('payment.html', yoco_public_key=os.getenv("YOCO_PUBLIC_KEY"), transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
