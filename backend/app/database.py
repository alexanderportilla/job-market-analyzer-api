
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# --- Database Configuration ---

# Use centralized configuration
DATABASE_URL = settings.DATABASE_URL

# Create engine with MySQL-specific arguments
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False  # Set to True for SQL debugging
)

# Each instance of the SessionLocal class will be a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models to inherit from.
Base = declarative_base()

# --- Dependency for getting a DB session ---

def get_db():
    """
    FastAPI dependency to get a database session for each request.
    Ensures the session is always closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
