
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    job_alerts = relationship("JobAlert", back_populates="user")
    saved_jobs = relationship("SavedJob", back_populates="user")

class JobOffer(Base):
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    company = Column(String(255))
    location = Column(String(255))
    description = Column(Text)
    url = Column(String(1000))
    source = Column(String(100))
    scraped_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    saved_jobs = relationship("SavedJob", back_populates="job_offer")

class JobAlert(Base):
    __tablename__ = "job_alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    keywords = Column(Text)  # JSON string of keywords
    location = Column(String(255))
    company = Column(String(255))
    frequency = Column(String(50), default="daily")  # daily, weekly, immediate
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_sent = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="job_alerts")

class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_offer_id = Column(Integer, ForeignKey("job_offers.id"))
    saved_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

    # Relationships
    user = relationship("User", back_populates="saved_jobs")
    job_offer = relationship("JobOffer", back_populates="saved_jobs")
