"""
Database session configuration.

Creates:
- engine
- session factory
- Base model
- FastAPI DB dependency
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for models
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a DB session
    and closes it after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

