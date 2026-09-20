import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Database URL
# ---------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")


# ---------------------------------------------------------
# Validate DATABASE_URL
# ---------------------------------------------------------

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not configured."
    )


# ---------------------------------------------------------
# PostgreSQL compatibility
#
# Render may provide:
#
# postgresql://...
#
# SQLAlchemy expects:
#
# postgresql+psycopg://...
#
# ---------------------------------------------------------

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )


# ---------------------------------------------------------
# SQLAlchemy Engine
# ---------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# ---------------------------------------------------------
# Session Factory
# ---------------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ---------------------------------------------------------
# Base Class
# ---------------------------------------------------------

Base = declarative_base()


# ---------------------------------------------------------
# Database Dependency
# ---------------------------------------------------------

def get_db():
    """
    FastAPI database dependency.

    Opens a database session for the request
    and closes it after the request is completed.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
