from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # ✅ For serving static files
from pydantic import BaseModel
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Import custom modules with error handling
try:
    from api.apk_generator import generate_apk
    logging.info("✅ apk_generator imported successfully!")
except ImportError as e:
    logging.error(f"❌ Error importing apk_generator: {e}")
    raise

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
    """Convert a website URL to an unsigned APK."""
    website_url = data.url

    if not website_url:
        raise HTTPException(status_code=400, detail="Missing website URL")

    try:
        apk_path = generate_apk(website_url, signed=False)  # Generate an unsigned APK
        return {"message": "APK generated successfully", "path": apk_path}
    except Exception as e:
        logging.error(f"❌ Error generating APK: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate APK")
