# main.py
#!pip install 'pydantic[email,timezone]'
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import jwt
import os
import requests
import hashlib
import base64


# Load secret key from env (default fallback for demo)
SECRET_KEY = "HHHQTQTHQahdJLWDFHGBKJDHEHFLJCHLJcVHL"
ALGORITHM = "HS256"

def generate_password_hash(password: str, salt: str) -> str:
    """
    Generate a SHA-256 hash of the combined password, salt, and email.

    Args:
        password (str): The user's password.
        salt (str): A unique salt string (should be random and stored per user).
        email (str): The user's email, used here to add uniqueness.

    Returns:
        str: Hexadecimal SHA-256 hash string.
    """
    # Combine password, salt, and email into one string
    combined = password + salt
    # Encode to bytes and hash using SHA-256
    hash_obj = hashlib.sha256(combined.encode('utf-8'))
    # Return the hex digest of the hash
    return hash_obj.hexdigest()


app = FastAPI()

# 1. Pydantic models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# 2. Mock password verification
def verify_password(plain_password: str, stored_password_hash: str, salt: str) -> bool:
    # In reality, you'd hash the plain_password and compare with stored hash
    password_hash = generate_password_hash(plain_password,salt)
    return password_hash == stored_password_hash


# 3. Fake user store
fake_user_db = {
    "saby@email.com": {
        "password_hash": "95714cdfbaee1645ceb1f14143236ed14176a52d8581ec38ea75a0198090e3fa",
        "salt":"g7PmbGq2j3DhE73UEnY/YQ=="
    },
    "manoj@email.com": {
        "password_hash": "9f7a14038b0d60ad4fb1a47a0479375e5a45a2a048f0572dd6c5e753b1e50b93",
        "salt":"Xw1JRSdLQHE52TpxJCjrug=="
    }
}

def create_jwt_token(user_email: str) -> str:
    # Token expiration time (e.g., 30 minutes from now)
    expire = datetime.utcnow() + timedelta(minutes=120)
    
    # Payload to encode
    payload = {
        "email": user_email,  # subject of the token
        "exp": expire
    }

    # Generate the token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# 5. Login endpoint
@app.post("/login", response_model=TokenResponse)
def login(form_data: LoginRequest):
    user = fake_user_db.get(form_data.email)
    if not user or not verify_password(form_data.password, user["password_hash"],user["salt"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_jwt_token(
        {"sub": form_data.email}
    )
    return {"access_token": token}
