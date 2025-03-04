from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import jwt
import sys
import logging
from dotenv import load_dotenv
from vercel_python import handler  # ✅ Fix for Vercel

# Get project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Add project and 'api' folder to sys.path
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, "api"))

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Import custom modules with error handling
try:
    from api.apk_generator import generate_apk
    logging.info("✅ apk_generator imported successfully!")
except ImportError as e:
    logging.error(f"❌ Error importing apk_generator: {e}")
    raise

try:
    from api.payment import verify_payment
    logging.info("✅ payment imported successfully!")
except ImportError as e:
    logging.error(f"❌ Error importing payment: {e}")
    raise

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Ensure JWT_SECRET_KEY is set
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("❌ JWT_SECRET_KEY is not set. Check your .env file.")

@app.route("/")
def home():
    """Test route to check if the server is running."""
    return jsonify({"message": "✅ Server is running on Vercel!"})

@app.route('/convert', methods=['POST'])
def convert():
    """Convert a website URL to an APK."""
    data = request.json
    website_url = data.get('url')

    if not website_url:
        return jsonify({"error": "Missing website URL"}), 400

    try:
        apk_path = generate_apk(website_url)
        return jsonify({"message": "APK generated successfully", "path": apk_path}), 200
    except Exception as e:
        logging.error(f"❌ Error generating APK: {e}")
        return jsonify({"error": "Failed to generate APK"}), 500

@app.route('/verify-payment', methods=['POST'])
def payment():
    """Verify a payment reference."""
    data = request.json
    payment_reference = data.get('reference')

    if not payment_reference:
        return jsonify({"error": "Missing payment reference"}), 400

    try:
        verified = verify_payment(payment_reference)

        if verified:
            token = jwt.encode({"premium": True}, SECRET_KEY, algorithm="HS256")
            return jsonify({"message": "Payment verified", "token": token}), 200
        else:
            return jsonify({"error": "Payment verification failed"}), 400
    except Exception as e:
        logging.error(f"❌ Error verifying payment: {e}")
        return jsonify({"error": "Failed to verify payment"}), 500

# Vercel handler (for deployment)
handler = handler(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
