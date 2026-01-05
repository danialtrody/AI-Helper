# ==============================
# DB Service - backend/services/db_service.py
# ==============================

from sqlalchemy.orm import Session
from backend.models import Chat, CV


# ==============================
# Get chat message
# ==============================
def get_chat(db, user_id: str, message: str) -> Chat | None:
    return (
        db.query(Chat)
        .filter(Chat.user_id == user_id, Chat.message == message)
        .first()
    )

# ==============================
# Save chat message
# ==============================
def save_message_to_db(db, user_id: str, message: str, reply: str) -> Chat:
    newMessage = Chat(user_id=user_id, message=message, reply=reply)
    db.add(newMessage)
    db.commit()
    db.refresh(newMessage)
    return newMessage

# ==============================
# Save CV
# ==============================
def save_cv_to_db(db: Session, user_id, filename: str, job_title: str, content: str, feedback: str):
    cv = CV(
        user_id=user_id,
        filename=filename,
        job_title=job_title,
        content=content,
        ai_feedback=feedback
    )
    db.add(cv)
    db.commit()
    db.refresh(cv)
    return cv
