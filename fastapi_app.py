from fastapi import FastAPI, Depends
from auth import create_jwt_token, verify_jwt_token

app = FastAPI()

@app.post("/login")
def login():
    """Mock login endpoint, returns a JWT token."""
    user_data = {"user_id": 123, "username": "test_user"}
    token = create_jwt_token(user_data)
    return {"access_token": token}

@app.get("/protected")
def protected_route(user_data: dict = Depends(verify_jwt_token)):
    """Protected endpoint requiring JWT authentication."""
    return {"message": "Welcome to the protected route!", "user": user_data}
