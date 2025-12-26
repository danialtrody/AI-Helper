from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# GEMINI_API_KEY=AIzaSyBCN2XZ2ZPbB8q2LKqaPd5sAgy_1w7i0-A
# GEMINI_API_KEY=AIzaSyBWkFuFmLw41ybBK6qEfSzmco-fYETM9Ds

load_dotenv()

SQLALCHEMY_DATABASE_URL = "sqlite:///chat.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
