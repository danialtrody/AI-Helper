import uuid

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    reply = Column(Text)
    user_id = Column(String, ForeignKey("users.id"))


class CV(Base):
    __tablename__ = "cv"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    filename = Column(String)
    job_title = Column(String)
    content = Column(Text)
    ai_feedback = Column(Text)

