
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class JobOffer(Base):
    """
    SQLAlchemy model for the 'job_offers' table.
    Represents a scraped job offer.
    """
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, nullable=True)
    location = Column(String, nullable=True)
    description = Column(Text)
    url = Column(String, unique=True) # The URL of the job offer
    source = Column(String) # The website it was scraped from (e.g., 'Computrabajo')
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<JobOffer(id={self.id}, title='{self.title}', company='{self.company}')>"
