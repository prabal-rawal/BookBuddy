from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

from models import User  # Corrected import

import secrets
import string

# Define the character set for the secret key
characters = string.ascii_letters + string.digits + string.punctuation

# Generate a random secret key with a length of 64 characters
secret_key = ''.join(secrets.choice(characters) for _ in range(64))

# Configuration
SECRET_KEY = secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password hashing and verification functions
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT token functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db, username: str, password: str):
    # Retrieve the user from the database
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False  # User not found
    if not verify_password(password, user.hashed_password):
        return False  # Incorrect password
    return user