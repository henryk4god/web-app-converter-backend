from fastapi import FastAPI, Depends
from auth import create_jwt_token, verify_jwt_token

app = FastAPI()

@app.post("/login")
def login():
    """
    User login endpoint (mock authentication).
    Returns a JWT token.
    """
    user_data = {"user_id": 123, "username": "test_user"}
    token = create_jwt_token(user_data)
    return {"access_token": token}

@app.get("/protected")
def protected_route(user_data: dict = Depends(verify_jwt_token)):
    """
    A protected endpoint that requires JWT authentication.
    """
    return {"message": "Welcome to the protected route!", "user": user_data}
