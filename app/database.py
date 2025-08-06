
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Database Configuration ---

# For the prototype, we use a simple SQLite database.
# The DATABASE_URL for PostgreSQL would look like:
# "postgresql://user:password@host:port/dbname"
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./job_market.db")

# The connect_args are only needed for SQLite.
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
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
