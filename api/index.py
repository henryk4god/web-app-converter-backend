from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import jwt
import requests
from dotenv import load_dotenv
from apk_generator import generate_apk
from payment import verify_payment

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    website_url = data.get('url')

    if not website_url:
        return jsonify({"error": "Missing website URL"}), 400

    try:
        apk_path = generate_apk(website_url)
        return jsonify({"message": "APK generated successfully", "path": apk_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/verify-payment', methods=['POST'])
def payment():
    data = request.json
    payment_reference = data.get('reference')

    if not payment_reference:
        return jsonify({"error": "Missing payment reference"}), 400

    verified = verify_payment(payment_reference)

    if verified:
        token = jwt.encode({"premium": True}, SECRET_KEY, algorithm="HS256")
        return jsonify({"message": "Payment verified", "token": token})
    else:
        return jsonify({"error": "Payment verification failed"}), 400

# Vercel handler
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
