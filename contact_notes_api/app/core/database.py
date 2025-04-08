from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from dotenv import load_dotenv
import os
from contextvars import ContextVar
import threading
from typing import Optional

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = scoped_session(session_factory)

Base = declarative_base()

# Use a context var to ensure thread safety
db_session: ContextVar[Optional[Session]] = ContextVar("db_session", default=None)

def get_db():
    session = SessionLocal()
    try:
        db_session.set(session)  # Set the session in context
        yield session
    finally:
        db_session.set(None)  # Clear the session from context
        session.close()
        SessionLocal.remove()  # Remove thread-local session