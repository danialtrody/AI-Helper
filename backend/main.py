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
from backend.models import Chat, User

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


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

# GET / -> serve index.html
@app.get("/")
async def displayIndex():
    return FileResponse(FRONTEND_DIR / "index.html")


# POST / -> chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest, db: db_dependency):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message is empty")

    try:
        print(f"[CHAT] New request | user_id={request.user_id}")

        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            user = User(id=request.user_id, username=request.user_id, hashed_password="")
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"[USER CREATED] id={user.id}")

        db_user_id = user.id

        # Cache
        cache_key = f"{db_user_id}:{request.message}"
        if cache_key in cache:
            print(f"[CACHE HIT] user_id={db_user_id}")
            return {"reply": cache[cache_key]}

        # DB check
        chat_row = (
            db.query(Chat)
            .filter(Chat.user_id == db_user_id, Chat.message == request.message)
            .first()
        )

        if chat_row:
            print(f"[DB HIT] message found | id={chat_row.id}")
            cache[cache_key] = chat_row.reply
            return {"reply": chat_row.reply}

        print("[AI] Sending request to Gemini model")

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=request.message
            )
            reply = response.text
        except Exception as e:
            print(f"[API ERROR] {str(e)}")
            reply = f"[MOCK RESPONSE] Echo: {request.message}"

        # Save to DB
        chat_history = Chat(user_id=db_user_id, message=request.message, reply=reply)
        db.add(chat_history)
        db.commit()
        db.refresh(chat_history)

        cache[cache_key] = reply

        print(f"[SUCCESS] Response saved | chat_id={chat_history.id}")
        return {"reply": reply}

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
