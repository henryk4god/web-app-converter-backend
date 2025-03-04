from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # ✅ For serving static files
from pydantic import BaseModel
import os
import jwt
import logging
import requests
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

# Ensure JWT_SECRET_KEY is set
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("❌ JWT_SECRET_KEY is not set. Check your .env file.")

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
if not PAYSTACK_SECRET_KEY:
    raise ValueError("❌ PAYSTACK_SECRET_KEY is not set. Check your .env file.")

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

class ConvertRequest(BaseModel):
    url: str

@app.post("/convert")
def convert(data: ConvertRequest):
    """Convert a website URL to an APK."""
    website_url = data.url

    if not website_url:
        raise HTTPException(status_code=400, detail="Missing website URL")

    try:
        apk_path = generate_apk(website_url)
        return {"message": "APK generated successfully", "path": apk_path}
    except Exception as e:
        logging.error(f"❌ Error generating APK: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate APK")

class PaymentRequest(BaseModel):
    reference: str

@app.post("/verify-payment")
def verify_payment(data: PaymentRequest):
    """Verify a payment reference."""
    payment_reference = data.reference

    if not payment_reference:
        raise HTTPException(status_code=400, detail="Missing payment reference")

    try:
        url = f"https://api.paystack.co/transaction/verify/{payment_reference}"
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        result = response.json()

        if response.status_code == 200 and result.get("data", {}).get("status") == "success":
            token = jwt.encode({"premium": True}, SECRET_KEY, algorithm="HS256")
            return {"message": "Payment verified", "token": token}
        else:
            raise HTTPException(status_code=400, detail="Payment verification failed")
    except Exception as e:
        logging.error(f"❌ Error verifying payment: {e}")
        raise HTTPException(status_code=500, detail="Failed to verify payment")
