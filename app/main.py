
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, scraper, analyzer
from .database import engine, get_db

# --- FastAPI Application Setup ---

# Create the database tables if they don't exist on startup.
# This is simple for a prototype, but for production, you might use Alembic for migrations.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Market Analyzer API",
    description="An API to scrape and analyze job market data for software developers in Colombia.",
    version="0.1.0",
)

# --- API Endpoints ---

@app.get("/", tags=["Root"], summary="Root endpoint of the API")
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Job Market Analyzer API!"}

@app.post("/scrape/", tags=["Scraping"], summary="Trigger the web scraper")
def trigger_scraping(pages: int = 1, db: Session = Depends(get_db)):
    """
    Starts the process of scraping job offers from Computrabajo.

    - **pages**: The number of result pages to scrape (default is 1).
    """
    if not 1 <= pages <= 10:
        raise HTTPException(status_code=400, detail="Number of pages must be between 1 and 10 for this demo.")
    
    result = scraper.scrape_job_offers(db=db, pages=pages)
    return result

@app.get("/stats/technologies/", response_model=List[schemas.TechnologyStat], tags=["Statistics"], summary="Get technology demand statistics")
def get_technology_stats(db: Session = Depends(get_db)):
    """
    Analyzes the stored job offers and returns a ranked list of the most in-demand technologies.
    """
    stats = analyzer.analyze_technology_demand(db=db)
    if not stats:
        return []
    return stats

@app.get("/offers/", response_model=List[schemas.JobOffer], tags=["Job Offers"], summary="Get all scraped job offers")
def get_all_offers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of all job offers currently stored in the database.

    - **skip**: Number of records to skip (for pagination).
    - **limit**: Maximum number of records to return.
    """
    offers = db.query(models.JobOffer).offset(skip).limit(limit).all()
    return offers

@app.get("/offers/search/", response_model=List[schemas.JobOffer], tags=["Job Offers"], summary="Search for offers by technology")
def search_offers_by_technology(technology: str, db: Session = Depends(get_db)):
    """
    Searches for job offers that mention a specific technology in their description.

    - **technology**: The technology to search for (e.g., 'Python', 'React').
    """
    # The '%' are wildcards for the LIKE query.
    search_term = f"%{technology.lower()}%"
    offers = db.query(models.JobOffer).filter(models.JobOffer.description.ilike(search_term)).all()
    if not offers:
        raise HTTPException(status_code=404, detail=f"No offers found mentioning '{technology}'")
    return offers
