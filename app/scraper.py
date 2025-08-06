
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from . import models, schemas

# --- Web Scraper for Job Portals ---

# We will target Computrabajo Colombia for this prototype.
# The URL is for software developer jobs.
# The URL is now for Python developer jobs.
BASE_URL = "https://www.computrabajo.com.co/ofertas-de-trabajo/?q=python"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_job_offers(db: Session, pages: int = 1):
    """
    Scrapes job offers from Computrabajo.

    Args:
        db: The database session.
        pages: The number of pages to scrape.
    """
    scraped_count = 0
    for page in range(1, pages + 1):
        # Construct the URL for the current page
        url = f"{BASE_URL}?p={page}"
        print(f"Scraping page: {url}")

        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue # Skip to the next page

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all job offer cards. The class name might change, this needs to be robust.
        offers = soup.find_all('article', class_='box_offer')

        if not offers:
            print("No offers found on page, stopping.")
            break

        for offer in offers:
            title_element = offer.find('a', class_='js-o-link')
            company_element = offer.find('a', class_='it-blank')
            location_element = offer.find('span', class_='list-location')
            description_element = offer.find('p', class_='parrafo')

            if not all([title_element, description_element]):
                continue # Skip if essential data is missing

            offer_url = "https://www.computrabajo.com.co" + title_element['href']

            # Check if the offer already exists in the DB
            existing_offer = db.query(models.JobOffer).filter(models.JobOffer.url == offer_url).first()
            if existing_offer:
                continue # Skip if we already have this offer

            job_data = schemas.JobOfferCreate(
                title=title_element.get_text(strip=True),
                company=company_element.get_text(strip=True) if company_element else "N/A",
                location=location_element.get_text(strip=True) if location_element else "N/A",
                description=description_element.get_text(strip=True),
                url=offer_url,
                source="Computrabajo"
            )

            db_offer = models.JobOffer(**job_data.dict())
            db.add(db_offer)
            scraped_count += 1

    db.commit()
    return {"message": f"Scraping complete. Added {scraped_count} new job offers."}
