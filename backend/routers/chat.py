# ==============================
# Chat Router - backend/routers/chat.py
# ==============================

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from google import genai

from backend.database import SessionLocal
from backend.models import User
from backend.services.auth_service import get_current_user
from backend.services.chat_service import generate_chat_feedback
from backend.services.db_service import get_chat, save_message_to_db

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
router = APIRouter(prefix="/chat", tags=["chat"])

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
# Request model
# ==============================
class ChatRequest(BaseModel):
    message: str

# ==============================
# In-memory cache
# ==============================
cache = {}

# ==============================
# Chat endpoint
# ==============================
@router.post("/", response_model=dict)
async def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message is empty")

    user_id = current_user.get("user_id")
    userName = current_user.get("username")
    print(f"[CHAT] New request | username={userName}")

    try:
        # --- Verify user exists in DB ---
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        cache_key = f"{user_id}:{message}"

        # --- Check cache first ---
        if cache_key in cache:
            print(f"[CACHE HIT] user_id={user_id}")
            reply = cache[cache_key]

        # --- Check DB ---
        elif chat_row := get_chat(db, user_id, message):
            print(f"[DB HIT] message found | id={chat_row.id}")
            reply = chat_row.reply
            cache[cache_key] = reply

        # --- Generate AI reply ---
        else:
            print("[AI] Sending request to Gemini model")
            reply = generate_chat_feedback(client, message)
            chat_row = save_message_to_db(db, user_id, message, reply)
            cache[cache_key] = reply
            print(f"[SUCCESS] Response saved | chat_id={chat_row.id}")

        return {"reply": reply}

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
