from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from documind.auth import register_user, login_user, decode_jwt

router = APIRouter(prefix="/api/auth")
security = HTTPBearer(auto_error=False)


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        raise HTTPException(401, "Not authenticated")
    payload = decode_jwt(credentials.credentials)
    if payload is None:
        raise HTTPException(401, "Invalid or expired token")
    return {
        "id": int(payload["sub"]),
        "username": payload["username"],
        "role": payload["role"],
    }


@router.post("/register")
def register(req: RegisterRequest):
    try:
        user = register_user(req.username, req.email, req.password)
        return {"status": "success", "user": user}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/login")
def login(req: LoginRequest):
    result = login_user(req.username, req.password)
    if result is None:
        raise HTTPException(401, "Invalid username or password")
    return result


@router.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    return current_user
