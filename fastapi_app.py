from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from api.apk_generator import generate_apk

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

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

@app.get("/")
def home():
    """Test route to check if the server is running."""
    return {"message": "✅ Server is running on Vercel!"}

class ConvertRequest(BaseModel):
    url: str

@app.post("/convert")
def convert(data: ConvertRequest):
    """Convert a website URL to an unsigned APK."""
    website_url = data.url

    if not website_url:
        raise HTTPException(status_code=400, detail="Missing website URL")

    logging.debug(f"Received URL: {website_url}")

    try:
        apk_path = generate_apk(website_url, signed=False)  # Generate an unsigned APK
        logging.debug(f"APK generated at path: {apk_path}")
        return {"message": "APK generated successfully", "path": apk_path}
    except Exception as e:
        logging.error(f"❌ Error generating APK: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate APK: {e}")
