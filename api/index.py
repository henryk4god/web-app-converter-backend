from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import custom modules
from apk_generator import generate_apk
from payment import verify_payment

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Ensure JWT_SECRET_KEY is set
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not set.")

@app.route('/convert', methods=['POST'])
def convert():
    """
    Endpoint to convert a website URL to an APK.
    """
    data = request.json
    website_url = data.get('url')

    if not website_url:
        return jsonify({"error": "Missing website URL"}), 400

    try:
        # Generate APK
        apk_path = generate_apk(website_url)
        return jsonify({"message": "APK generated successfully", "path": apk_path}), 200
    except Exception as e:
        # Log the error and return a 500 response
        print(f"Error generating APK: {e}")
        return jsonify({"error": "Failed to generate APK. Please try again later."}), 500

@app.route('/verify-payment', methods=['POST'])
def payment():
    """
    Endpoint to verify a payment reference.
    """
    data = request.json
    payment_reference = data.get('reference')

    if not payment_reference:
        return jsonify({"error": "Missing payment reference"}), 400

    try:
        # Verify payment
        verified = verify_payment(payment_reference)

        if verified:
            # Generate JWT token for premium access
            token = jwt.encode({"premium": True}, SECRET_KEY, algorithm="HS256")
            return jsonify({"message": "Payment verified", "token": token}), 200
        else:
            return jsonify({"error": "Payment verification failed"}), 400
    except Exception as e:
        # Log the error and return a 500 response
        print(f"Error verifying payment: {e}")
        return jsonify({"error": "Failed to verify payment. Please try again later."}), 500

# Vercel serverless handler
def handler(event, context):
    """
    Vercel serverless function handler.
    """
    from vercel_lambda.wsgi import Response
    return Response(app, event, context)

if __name__ == '__main__':
    # Run the Flask app in development mode
    app.run(host="0.0.0.0", port=8000, debug=True)