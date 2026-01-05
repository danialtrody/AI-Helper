# ==============================
# Chat Router - backend/routers/auth.py
# ==============================
from http.client import HTTPException

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.services.auth_service import create_access_token, create_user, verify_user, get_db, CreateUser

# ==============================
# Router setup
# ==============================
router = APIRouter(prefix="/auth", tags=["auth"])

# ==============================
# Register endpoint
# ==============================
@router.post("/register")
async def register_user(create_user_request: CreateUser, db: Session = Depends(get_db)):
    return await create_user(create_user_request, db)

# ==============================
# Login endpoint
# ==============================
@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = verify_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.username, user.id)
    return {"access_token": token, "token_type": "bearer"}
