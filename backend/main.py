from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from backend.routers import chat, cv

app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
# Include routers
app.include_router(cv.router)


# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR.parent / "frontend/templates"
STATIC_DIR = BASE_DIR.parent / "frontend/static"

# --- Templates ---
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# --- Static ---
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# --- Routes ---
@app.get("/")
async def chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cv")
async def cv(request: Request):
    return templates.TemplateResponse("cv.html", {"request": request})
