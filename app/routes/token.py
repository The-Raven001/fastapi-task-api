from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

"""
   Creates a signed JWT access token with an expiration time.

    - Copies the provided payload data to avoid mutation
    - Adds an "exp" (expiration) claim using UTC time
    - Signs the token using the application's SECRET_KEY and HS256 algorithm

The resulting token is used for authenticating protected API endpoints.

Args:
    data (dict): Payload data to encode in the token (e.g., {"sub": user_id})

Returns:
    str: Encoded JWT access token

Security:
    - The token becomes invalid after expiration
    - SECRET_KEY must remain private
    - Token payload should not contain sensitive data
 """