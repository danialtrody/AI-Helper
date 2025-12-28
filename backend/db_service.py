from backend.models import User, Chat

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
