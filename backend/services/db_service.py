from sqlalchemy.orm import Session

from backend.models import User, Chat, CV


def get_or_create_user(db, user_id: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, username=user_id, hashed_password="")
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"[USER CREATED] id={user.id}")
    return user

def get_chat(db, user_id: str, message: str) -> Chat | None:
    return (
        db.query(Chat)
        .filter(Chat.user_id == user_id, Chat.message == message)
        .first()
    )

def addMessageToDB(db, user_id: str, message: str, reply: str) -> Chat:
    newMessage = Chat(user_id=user_id, message=message, reply=reply)
    db.add(newMessage)
    db.commit()
    db.refresh(newMessage)
    return newMessage

def save_cv_to_db(db: Session, user_id: str, filename: str, job_title: str, content: str, feedback: str):
    """Save the CV and AI feedback to the database."""
    user = get_or_create_user(db, user_id)
    cv = CV(
        user_id=user.id,
        filename=filename,
        job_title=job_title,
        content=content,
        ai_feedback=feedback
    )
    db.add(cv)
    db.commit()
    db.refresh(cv)
    return cv

