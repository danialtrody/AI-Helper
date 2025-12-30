# backend/routers/cv.py
from fastapi import APIRouter, HTTPException, Depends, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from backend.database import SessionLocal
from backend.services import cv_service, db_service
from dotenv import load_dotenv
from google import genai
import os

# Load environment variables
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter(prefix="/cv", tags=["cv"])
templates = Jinja2Templates(directory="frontend/templates")

# --- DB dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Render CV page ---
@router.get("")
def render_cv_page(request: Request):

    return templates.TemplateResponse("cv.html", {"request": request})

# --- Upload CV endpoint ---
@router.post("/upload")
async def upload_cv(
    job_title: str = Form(...),
    user_id: str = Form("guest"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # 1. Read file content
        content = await cv_service.read_cv_file(file)

        # 2. Generate AI feedback
        feedback = cv_service.generate_cv_feedback(content, job_title, client)

        # 3. Save CV in DB
        cv = db_service.save_cv_to_db(db, user_id, file.filename, job_title, content, feedback)

        return {"cv_id": cv.id, "feedback": feedback}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
