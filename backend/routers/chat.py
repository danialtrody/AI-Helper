# backend/routers/chat.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from google import genai

from backend.database import SessionLocal
from backend.services.chat_service import generate_chat_feedback
from backend.services.db_service import get_chat, get_or_create_user, save_message_to_db

# --- Load environment variables ---
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- Router setup ---
router = APIRouter(prefix="/chat", tags=["chat"])


# --- DB dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Request model ---
class ChatRequest(BaseModel):
    message: str
    user_id: str = "guest"

# --- In-memory cache ---
cache = {}

# --- Chat endpoint ---
@router.post("")
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):

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
            reply = generate_chat_feedback(client, request.message)
            # Save to DB
            chat_row = save_message_to_db(db, db_user_id, request.message, reply)
            cache[cache_key] = reply
            print(f"[SUCCESS] Response saved | chat_id={chat_row.id}")

        return {"reply": reply}

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
