# ==============================
# FastAPI Main Application - backend/app.py
# ==============================

from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.routers import chat, cv


app = FastAPI()

# ==============================
# CORS Middleware
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Include Routers
# ==============================
app.include_router(chat.router)
app.include_router(cv.router)

# ==============================
# Paths for Templates and Static Files
# ==============================
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR.parent / "frontend/templates"
STATIC_DIR = BASE_DIR.parent / "frontend/static"

# ==============================
# Templates Setup
# ==============================
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ==============================
# Static Files Setup
# ==============================
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ==============================
# Routes
# ==============================
@app.get("/")
async def chat(request: Request):
    """Render the chat page."""
    current_year = datetime.now().year
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "current_year": current_year}
    )

@app.get("/cv")
async def cv(request: Request):
    """Render the CV page."""
    current_year = datetime.now().year
    return templates.TemplateResponse(
        "cv.html",
        {"request": request, "current_year": current_year}
    )
