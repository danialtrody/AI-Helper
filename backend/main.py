from fastapi import FastAPI, HTTPException , Depends
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from models import Chat, User
from database import Base, engine
from fastapi.staticfiles import StaticFiles
from pathlib import Path


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# יצירת טבלאות אם לא קיימות
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



BASE_DIR = Path(__file__).resolve().parent  # backend/
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class ChatRequest(BaseModel):
    message: str
    user_id: str = "guest"

cache = {}

@app.post("/chat")
async def chat(request: ChatRequest, db: db_dependency):

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message is empty")

    try:
        print(f"[CHAT] New request | user_id={request.user_id}")

        # בדיקה אם המשתמש קיים, אם לא – צור אותו
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            user = User(id=request.user_id, username=request.user_id, hashed_password="")
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"[USER CREATED] id={user.id}")

        # שימוש במזהה משתמש מאומת
        db_user_id = user.id

        # Cache
        cache_key = f"{db_user_id}:{request.message}"
        if cache_key in cache:
            print(f"[CACHE HIT] user_id={db_user_id}")
            return {"reply": cache[cache_key]}

        # DB check
        chat_row = (
            db.query(Chat)
            .filter(
                Chat.user_id == db_user_id,
                Chat.message == request.message
            )
            .first()
        )

        if chat_row:
            print(f"[DB HIT] message found | id={chat_row.id}")
            cache[cache_key] = chat_row.reply
            return {"reply": chat_row.reply}

        print("[AI] Sending request to Gemini model")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.message
        )

        reply = response.text

        # Save to DB
        chat_history = Chat(
            user_id=db_user_id,
            message=request.message,
            reply=reply
        )

        db.add(chat_history)
        db.commit()
        db.refresh(chat_history)

        cache[cache_key] = reply

        print(f"[SUCCESS] Response saved | chat_id={chat_history.id}")
        return {"reply": reply}

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
