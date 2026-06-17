import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import bcrypt
import jwt

from documind.config import Config
from documind.database import UserDB

JWT_SECRET = os.getenv("JWT_SECRET", "documind-super-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_jwt(user_id: int, username: str, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRY_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_jwt(token: str) -> Optional[Dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def register_user(username: str, email: str, password: str, role: str = "user") -> Dict:
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters")
    if not username or len(username) < 3:
        raise ValueError("Username must be at least 3 characters")

    db = UserDB()
    existing = db.get_user_by_username(username)
    if existing:
        raise ValueError("Username already taken")
    existing_email = db.get_user_by_email(email)
    if existing_email:
        raise ValueError("Email already registered")

    hashed = hash_password(password)
    user = db.create_user(username, email, hashed, role)
    user.pop("hashed_password", None)
    return user


def login_user(username: str, password: str) -> Optional[Dict]:
    db = UserDB()
    user = db.get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    token = create_jwt(user["id"], user["username"], user["role"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
        },
    }
