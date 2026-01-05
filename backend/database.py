# ==============================
# Database Setup - backend/database.py
# ==============================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ==============================
# Database URL
# ==============================
SQLALCHEMY_DATABASE_URL = "sqlite:///chat.db"

# ==============================
# SQLAlchemy Engine
# ==============================
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# ==============================
# Session Local
# ==============================
# Create session factory for dependency injection
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ==============================
# Base Class for Models
# ==============================
Base = declarative_base()
