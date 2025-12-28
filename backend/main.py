from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated
from pathlib import Path
from dotenv import load_dotenv
import os
from google import genai

from backend.database import SessionLocal, Base, engine
from backend.db_service import get_chat, get_or_create_user, addMessageToDB
from backend.ai_service import generate_reply

# Load environment variables and initialize Gemini client
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (frontend)
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Request model
class ChatRequest(BaseModel):
    message: str
    user_id: str = "guest"

# In-memory cache
cache = {}

# Routes
@app.get("/")
async def display_index():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/chat")
async def chat(request: ChatRequest, db: db_dependency):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message is empty")

    print(f"[CHAT] New request | user_id={request.user_id}")

    try:
        # Get or create user
        user = get_or_create_user(db, request.user_id)
        db_user_id = user.id
        cache_key = f"{db_user_id}:{request.message}"

        # Check cache first
        if cache_key in cache:
            print(f"[CACHE HIT] user_id={db_user_id}")
            reply = cache[cache_key]

        # Check DB
        elif chat_row := get_chat(db, db_user_id, request.message):
            print(f"[DB HIT] message found | id={chat_row.id}")
            reply = chat_row.reply
            cache[cache_key] = reply

        # Generate AI reply
        else:
            print("[AI] Sending request to Gemini model")
            reply = generate_reply(client, request.message)
            # Save to DB
            chat_row = addMessageToDB(db, db_user_id, request.message, reply)
            cache[cache_key] = reply
            print(f"[SUCCESS] Response saved | chat_id={chat_row.id}")

        return {"reply": reply}

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
