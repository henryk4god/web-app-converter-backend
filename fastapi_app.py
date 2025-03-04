from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # ✅ Added for serving static files
import os
import jwt
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)

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

# Ensure JWT_SECRET_KEY is set
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("❌ JWT_SECRET_KEY is not set. Check your .env file.")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static files (like favicon.png)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    """Test route to check if the server is running."""
    return {"message": "✅ Server is running on Vercel!"}

@app.post("/convert")
def convert(data: dict):
    """Convert a website URL to an APK."""
    website_url = data.get('url')

    if not website_url:
        raise HTTPException(status_code=400, detail="Missing website URL")

    try:
        apk_path = generate_apk(website_url)
        return {"message": "APK generated successfully", "path": apk_path}
    except Exception as e:
        logging.error(f"❌ Error generating APK: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate APK")

@app.post("/verify-payment")
def payment(data: dict):
    """Verify a payment reference."""
    payment_reference = data.get('reference')

    if not payment_reference:
        raise HTTPException(status_code=400, detail="Missing payment reference")

    try:
        verified = verify_payment(payment_reference)

        if verified:
            token = jwt.encode({"premium": True}, SECRET_KEY, algorithm="HS256")
            return {"message": "Payment verified", "token": token}
        else:
            raise HTTPException(status_code=400, detail="Payment verification failed")
    except Exception as e:
        logging.error(f"❌ Error verifying payment: {e}")
        raise HTTPException(status_code=500, detail="Failed to verify payment")
