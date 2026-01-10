# ==============================
# FastAPI Main Application - backend/app.py
# ==============================

from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.database import Base, engine
from backend.routers import chat, cv, auth

# ==============================
# FastAPI App Initialization
# ==============================
app = FastAPI()

Base.metadata.create_all(bind=engine)

# ==============================
# CORS Middleware
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Include Routers
# ==============================
app.include_router(chat.router)
app.include_router(cv.router)
app.include_router(auth.router)

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
    current_year = datetime.now().year
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "current_year": current_year}
    )

@app.get("/chat")
async def chat_page(request: Request):
    current_year = datetime.now().year
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "current_year": current_year}
    )

@app.get("/cv")
async def cv_page(request: Request):
    current_year = datetime.now().year
    return templates.TemplateResponse(
        "cv.html",
        {"request": request, "current_year": current_year}
    )

@app.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/health")
def health_check():
    return {"status": "ok"}
