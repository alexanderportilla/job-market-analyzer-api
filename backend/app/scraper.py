
import logging
import time
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from . import models, schemas
from .config import settings

# Configure logging
logger = logging.getLogger(__name__)

# --- Web Scraper for Job Portals ---

# Use centralized configuration
BASE_URL = settings.BASE_URL
HEADERS = settings.HEADERS

def scrape_job_offers(db: Session, pages: int = 1):
    """
    Scrapes job offers from Computrabajo and saves them to MySQL database.

    Args:
        db: The database session.
        pages: The number of pages to scrape.
    """
    scraped_count = 0
    total_processed = 0
    
    logger.info(f"🚀 Starting scraping process for {pages} pages...")
    
    for page in range(1, pages + 1):
        # Construct the URL for the current page
        url = f"{BASE_URL}?p={page}"
        logger.info(f"📄 Scraping page {page}/{pages}: {url}")

        try:
            response = requests.get(url, headers=HEADERS, timeout=settings.REQUEST_TIMEOUT)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        except requests.RequestException as e:
            logger.error(f"❌ Error fetching page {page}: {e}")
            continue # Skip to the next page

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all job offer cards. The class name might change, this needs to be robust.
        offers = soup.find_all('article', class_='box_offer')

        if not offers:
            logger.warning(f"⚠️ No offers found on page {page}, stopping.")
            break

        page_count = 0
        for offer in offers:
            total_processed += 1
            
            try:
                title_element = offer.find('a', class_='js-o-link')
                company_element = offer.find('a', class_='it-blank')
                location_element = offer.find('span', class_='list-location')
                description_element = offer.find('p', class_='parrafo')

                if not all([title_element, description_element]):
                    logger.debug(f"⏭️ Skipping offer {total_processed}: missing essential data")
                    continue # Skip if essential data is missing

                offer_url = "https://www.computrabajo.com.co" + title_element['href']

                # Check if the offer already exists in the DB
                existing_offer = db.query(models.JobOffer).filter(models.JobOffer.url == offer_url).first()
                if existing_offer:
                    logger.debug(f"⏭️ Job already exists: {title_element.get_text(strip=True)}")
                    continue # Skip if we already have this offer

                job_data = schemas.JobOfferCreate(
                    title=title_element.get_text(strip=True),
                    company=company_element.get_text(strip=True) if company_element else "N/A",
                    location=location_element.get_text(strip=True) if location_element else "N/A",
                    description=description_element.get_text(strip=True),
                    url=offer_url,
                    source="Computrabajo"
                )

                # Create and save the job offer
                db_offer = models.JobOffer(**job_data.dict())
                db.add(db_offer)
                scraped_count += 1
                page_count += 1
                
                logger.info(f"💾 Saved new job: {job_data.title} at {job_data.company}")
                
            except Exception as e:
                logger.error(f"❌ Error processing offer {total_processed}: {e}")
                continue

        # Commit after each page to avoid losing all data if there's an error
        try:
            db.commit()
            logger.info(f"✅ Page {page} completed: {page_count} new offers saved")
        except SQLAlchemyError as e:
            logger.error(f"❌ Database error on page {page}: {e}")
            db.rollback()
            continue

        # Add delay between pages to be respectful to the server
        if page < pages:
            time.sleep(settings.DELAY_BETWEEN_REQUESTS)
    
    logger.info(f"🎉 Scraping complete! Processed {total_processed} offers, saved {scraped_count} new job offers to MySQL.")
    return {
        "message": f"Scraping complete. Processed {total_processed} offers, added {scraped_count} new job offers to MySQL.",
        "total_processed": total_processed,
        "new_offers": scraped_count,
        "timestamp": datetime.now().isoformat()
    }

def save_job_offers_to_mysql(job_data_list: list, db: Session):
    """
    Save a list of job offers to MySQL database.
    
    Args:
        job_data_list: List of job offer dictionaries
        db: Database session
    """
    saved_count = 0
    skipped_count = 0
    
    logger.info(f"💾 Saving {len(job_data_list)} job offers to MySQL...")
    
    for job_data in job_data_list:
        try:
            # Check if job already exists
            existing = db.query(models.JobOffer).filter(models.JobOffer.url == job_data["url"]).first()
            
            if not existing:
                job_offer = models.JobOffer(**job_data)
                db.add(job_offer)
                saved_count += 1
                logger.debug(f"✅ Saved: {job_data['title']} at {job_data['company']}")
            else:
                skipped_count += 1
                logger.debug(f"⏭️ Skipped (exists): {job_data['title']}")
                
        except Exception as e:
            logger.error(f"❌ Error saving job {job_data.get('title', 'Unknown')}: {e}")
            continue
    
    try:
        db.commit()
        logger.info(f"✅ Successfully saved {saved_count} new job offers to MySQL (skipped {skipped_count})")
        return saved_count
    except SQLAlchemyError as e:
        logger.error(f"❌ Database commit error: {e}")
        db.rollback()
        return 0

def get_database_stats(db: Session):
    """
    Get statistics about the job offers in the database.
    
    Args:
        db: Database session
    """
    try:
        total_offers = db.query(models.JobOffer).count()
        unique_companies = db.query(models.JobOffer.company).distinct().count()
        
        # Recent offers (last 24 hours)
        yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        recent_offers = db.query(models.JobOffer).filter(
            models.JobOffer.scraped_at >= yesterday
        ).count()
        
        # Top companies
        from sqlalchemy import func
        top_companies = db.query(
            models.JobOffer.company,
            func.count(models.JobOffer.id).label('count')
        ).filter(
            models.JobOffer.company.isnot(None)
        ).group_by(
            models.JobOffer.company
        ).order_by(
            func.count(models.JobOffer.id).desc()
        ).limit(5).all()
        
        return {
            "total_offers": total_offers,
            "unique_companies": unique_companies,
            "recent_offers_24h": recent_offers,
            "top_companies": [{"company": company, "count": count} for company, count in top_companies],
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting database stats: {e}")
        return {}

def cleanup_old_offers(db: Session, days: int = 30):
    """
    Remove job offers older than specified days.
    
    Args:
        db: Database session
        days: Number of days to keep offers
    """
    try:
        cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - days)
        
        old_offers = db.query(models.JobOffer).filter(
            models.JobOffer.scraped_at < cutoff_date
        ).all()
        
        count = len(old_offers)
        for offer in old_offers:
            db.delete(offer)
        
        db.commit()
        logger.info(f"🗑️ Cleaned up {count} old job offers (older than {days} days)")
        return count
        
    except Exception as e:
        logger.error(f"❌ Error cleaning up old offers: {e}")
        db.rollback()
        return 0

def export_job_offers_to_csv(db: Session, filename: str = None):
    """
    Export job offers to CSV file.
    
    Args:
        db: Database session
        filename: Output filename (optional)
    """
    import csv
    from datetime import datetime
    
    if not filename:
        filename = f"job_offers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        offers = db.query(models.JobOffer).all()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'title', 'company', 'location', 'description', 'url', 'source', 'scraped_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for offer in offers:
                writer.writerow({
                    'id': offer.id,
                    'title': offer.title,
                    'company': offer.company,
                    'location': offer.location,
                    'description': offer.description,
                    'url': offer.url,
                    'source': offer.source,
                    'scraped_at': offer.scraped_at.isoformat()
                })
        
        logger.info(f"📄 Exported {len(offers)} job offers to {filename}")
        return filename
        
    except Exception as e:
        logger.error(f"❌ Error exporting to CSV: {e}")
        return None
