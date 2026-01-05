# ==============================
# Auth Service - backend/services/auth_service.py
# ==============================

import os
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
import jwt
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from backend.database import SessionLocal
from backend.models import User

# ==============================
# Load environment variables
# ==============================
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

bcrypt_context = CryptContext(schemes=["argon2"], deprecated="auto")

# ==============================
# OAuth2 (JWT Dependency)
# ==============================
from fastapi.security import OAuth2PasswordBearer

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# ==============================
# Pydantic Models
# ==============================
class CreateUser(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# ==============================
# Database Dependency
# ==============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# ==============================
# JWT Functions
# ==============================
def create_access_token(username: str, user_id: str, expire_delta: timedelta = None):
    if expire_delta is None:
        expire_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"username": username, "user_id": user_id}
    expires = datetime.now(timezone.utc) + expire_delta
    payload.update({"exp": expires})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# ==============================
# User CRUD & Auth Functions
# ==============================
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def verify_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user

async def create_user(create_user: CreateUser, db: db_dependency):
    if get_user_by_username(db, create_user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    user_model = User(
        username=create_user.username,
        hashed_password=bcrypt_context.hash(create_user.password),
    )

    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return {"message": "User created successfully", "user_id": user_model.id}

# ==============================
# JWT Verification Dependency
# ==============================
async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: str = payload.get("user_id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return {"username": username, "user_id": user_id}
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
