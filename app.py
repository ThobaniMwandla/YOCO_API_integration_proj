import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Yoco API details
YOCO_SECRET_KEY = os.getenv("YOCO_SECRET_KEY")
YOCO_ENDPOINT = "https://online.yoco.com/v1/charges/"

@app.route("/")
def payment_page():
    """Render payment page"""
    return render_template("payment.html", yoco_public_key=os.getenv("YOCO_PUBLIC_KEY"))

@app.route("/pay", methods=["POST"])
def process_payment():
    """Handles Yoco payment request"""
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Payment token is required"}), 400

    response = requests.post(
        YOCO_ENDPOINT,
        headers={"X-Auth-Secret-Key": YOCO_SECRET_KEY},
        json={"token": token, "amountInCents": 5000, "currency": "ZAR"},
    )
    print("******************************************")
    print(response.json())
    print(response.status_code)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
