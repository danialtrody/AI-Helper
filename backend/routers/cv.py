# ==============================
# CV Router - backend/routers/cv.py
# ==============================

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.services import cv_service, db_service
from dotenv import load_dotenv
from google import genai
import os

from backend.services.auth_service import get_current_user

# ==============================
# Load environment variables
# ==============================
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment variables")

client = genai.Client(api_key=GEMINI_API_KEY)

# ==============================
# Router setup
# ==============================
router = APIRouter(prefix="/cv", tags=["cv"])

# ==============================
# DB dependency
# ==============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==============================
# Upload CV endpoint
# ==============================
@router.post("/upload")
async def upload_cv(
    job_title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    content = await cv_service.read_cv_file(file)
    feedback = cv_service.generate_cv_feedback(content, job_title, client)
    cv = db_service.save_cv_to_db(db, user_id, file.filename, job_title, content, feedback)
    return {"cv_id": cv.id, "feedback": feedback}
