from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import psycopg2
import os
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: str = "guest"

cache = {}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        if request.message in cache:
            return {"reply": cache[request.message]}

        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT reply FROM chat_history WHERE message=%s LIMIT 1",
                    (request.message,)
                )
                result = cursor.fetchone()
                if result:
                    reply = result[0]
                    cache[request.message] = reply
                    return {"reply": reply}


        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.message
        )
        reply = response.text


        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO chat_history (user_id, message, reply) VALUES (%s, %s, %s)",
                    (request.user_id, request.message, reply)
                )
                conn.commit()

        cache[request.message] = reply

        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
