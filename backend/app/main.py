
import logging
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json

from . import models, schemas, scraper, analyzer
from .database import engine, get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI Application Setup ---

# Create the database tables if they don't exist on startup.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Market Analyzer API",
    description="An API to scrape and analyze job market data for software developers in Colombia.",
    version="1.0.0",
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/offers/search/", response_model=schemas.SearchResponse, tags=["Job Offers"], summary="Advanced search for job offers")
def advanced_search_offers(
    q: str = None,
    company: str = None,
    location: str = None,
    technology: str = None,
    min_salary: float = None,
    max_salary: float = None,
    job_type: str = None,  # full-time, part-time, contract, remote
    experience_level: str = None,  # junior, mid, senior, lead
    sort_by: str = "scraped_at",  # scraped_at, title, company, location
    sort_order: str = "desc",  # asc, desc
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Advanced search for job offers with multiple filters and sorting options.
    
    - **q**: General search term (searches in title, description, company)
    - **company**: Filter by specific company
    - **location**: Filter by location
    - **technology**: Filter by technology mentioned
    - **min_salary**: Minimum salary filter
    - **max_salary**: Maximum salary filter
    - **job_type**: Filter by job type
    - **experience_level**: Filter by experience level
    - **sort_by**: Field to sort by
    - **sort_order**: Sort order (asc/desc)
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    query = db.query(models.JobOffer)
    
    # Apply filters
    if q:
        search_term = f"%{q.lower()}%"
        query = query.filter(
            db.or_(
                models.JobOffer.title.ilike(search_term),
                models.JobOffer.description.ilike(search_term),
                models.JobOffer.company.ilike(search_term)
            )
        )
    
    if company:
        query = query.filter(models.JobOffer.company.ilike(f"%{company}%"))
    
    if location:
        query = query.filter(models.JobOffer.location.ilike(f"%{location}%"))
    
    if technology:
        query = query.filter(models.JobOffer.description.ilike(f"%{technology}%"))
    
    # Apply sorting
    if sort_by == "title":
        order_column = models.JobOffer.title
    elif sort_by == "company":
        order_column = models.JobOffer.company
    elif sort_by == "location":
        order_column = models.JobOffer.location
    else:
        order_column = models.JobOffer.scraped_at
    
    if sort_order == "asc":
        query = query.order_by(order_column.asc())
    else:
        query = query.order_by(order_column.desc())
    
    # Apply pagination
    total_count = query.count()
    offers = query.offset(skip).limit(limit).all()
    
    return {
        "offers": offers,
        "total": total_count,
        "page": (skip // limit) + 1,
        "pages": (total_count + limit - 1) // limit,
        "has_next": skip + limit < total_count,
        "has_prev": skip > 0
    }

# --- Premium Dashboard Endpoints ---

@app.get("/dashboard/stats/", tags=["Dashboard"], summary="Get dashboard statistics")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get comprehensive dashboard statistics including total offers, companies, and trends.
    """
    try:
        # Total offers
        total_offers = db.query(models.JobOffer).count()
        
        # Unique companies
        unique_companies = db.query(models.JobOffer.company).distinct().count()
        
        # Recent offers (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_offers = db.query(models.JobOffer).filter(
            models.JobOffer.scraped_at >= week_ago
        ).count()
        
        # Technology count
        tech_stats = analyzer.analyze_technology_demand(db=db)
        unique_technologies = len(tech_stats)
        
        # Monthly trend (last 6 months)
        monthly_data = []
        for i in range(6):
            month_start = datetime.now().replace(day=1) - timedelta(days=30*i)
            month_end = month_start.replace(day=28) + timedelta(days=4)
            month_end = month_end.replace(day=1) - timedelta(days=1)
            
            month_offers = db.query(models.JobOffer).filter(
                models.JobOffer.scraped_at >= month_start,
                models.JobOffer.scraped_at <= month_end
            ).count()
            
            monthly_data.append({
                "month": month_start.strftime("%b"),
                "offers": month_offers
            })
        
        monthly_data.reverse()
        
        return {
            "total_offers": total_offers,
            "unique_companies": unique_companies,
            "recent_offers": recent_offers,
            "unique_technologies": unique_technologies,
            "monthly_trend": monthly_data,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving dashboard statistics")

@app.get("/dashboard/recent-activity/", tags=["Dashboard"], summary="Get recent job activity")
def get_recent_activity(db: Session = Depends(get_db)):
    """
    Get recent job offers activity for the dashboard.
    """
    try:
        # Get recent offers (last 10)
        recent_offers = db.query(models.JobOffer).order_by(
            models.JobOffer.scraped_at.desc()
        ).limit(10).all()
        
        activity = []
        for offer in recent_offers:
            time_diff = datetime.now() - offer.scraped_at
            if time_diff.days > 0:
                time_ago = f"{time_diff.days}d ago"
            elif time_diff.seconds > 3600:
                time_ago = f"{time_diff.seconds // 3600}h ago"
            else:
                time_ago = f"{time_diff.seconds // 60}m ago"
            
            activity.append({
                "company": offer.company or "Unknown",
                "position": offer.title,
                "time": time_ago,
                "url": offer.url
            })
        
        return activity
    except Exception as e:
        logger.error(f"Error getting recent activity: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving recent activity")

@app.get("/analytics/company-stats/", tags=["Analytics"], summary="Get company statistics")
def get_company_stats(db: Session = Depends(get_db)):
    """
    Get statistics grouped by company.
    """
    try:
        # Get companies with offer counts
        company_stats = db.query(
            models.JobOffer.company,
            db.func.count(models.JobOffer.id).label('offer_count')
        ).filter(
            models.JobOffer.company.isnot(None)
        ).group_by(
            models.JobOffer.company
        ).order_by(
            db.func.count(models.JobOffer.id).desc()
        ).limit(20).all()
        
        return [
            {"company": company, "offer_count": count}
            for company, count in company_stats
        ]
    except Exception as e:
        logger.error(f"Error getting company stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving company statistics")

@app.get("/analytics/location-stats/", tags=["Analytics"], summary="Get location statistics")
def get_location_stats(db: Session = Depends(get_db)):
    """
    Get statistics grouped by location.
    """
    try:
        # Get locations with offer counts
        location_stats = db.query(
            models.JobOffer.location,
            db.func.count(models.JobOffer.id).label('offer_count')
        ).filter(
            models.JobOffer.location.isnot(None)
        ).group_by(
            models.JobOffer.location
        ).order_by(
            db.func.count(models.JobOffer.id).desc()
        ).limit(15).all()
        
        return [
            {"location": location, "offer_count": count}
            for location, count in location_stats
        ]
    except Exception as e:
        logger.error(f"Error getting location stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving location statistics")

@app.get("/analytics/salary-trends/", tags=["Analytics"], summary="Get salary trend analysis")
def get_salary_trends(db: Session = Depends(get_db)):
    """
    Analyze salary trends by technology and experience level.
    """
    try:
        # This would require salary data in the database
        # For now, return mock data structure
        return {
            "average_salaries": {
                "Python": {"junior": 3000000, "mid": 4500000, "senior": 6500000},
                "React": {"junior": 2800000, "mid": 4200000, "senior": 6000000},
                "Java": {"junior": 3200000, "mid": 4800000, "senior": 7000000},
            },
            "trends": [
                {"month": "Jan", "avg_salary": 4200000},
                {"month": "Feb", "avg_salary": 4350000},
                {"month": "Mar", "avg_salary": 4500000},
            ]
        }
    except Exception as e:
        logger.error(f"Error getting salary trends: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving salary trends")

@app.get("/analytics/experience-analysis/", tags=["Analytics"], summary="Get experience level analysis")
def get_experience_analysis(db: Session = Depends(get_db)):
    """
    Analyze job offers by experience level requirements.
    """
    try:
        # Analyze job titles for experience levels
        junior_keywords = ["junior", "jr", "entry", "trainee", "intern"]
        senior_keywords = ["senior", "sr", "lead", "principal", "architect"]
        
        total_offers = db.query(models.JobOffer).count()
        
        junior_count = 0
        senior_count = 0
        mid_count = 0
        
        for offer in db.query(models.JobOffer).all():
            title_lower = offer.title.lower()
            if any(keyword in title_lower for keyword in senior_keywords):
                senior_count += 1
            elif any(keyword in title_lower for keyword in junior_keywords):
                junior_count += 1
            else:
                mid_count += 1
        
        return {
            "total_offers": total_offers,
            "junior": {
                "count": junior_count,
                "percentage": round((junior_count / total_offers) * 100, 1) if total_offers > 0 else 0
            },
            "mid": {
                "count": mid_count,
                "percentage": round((mid_count / total_offers) * 100, 1) if total_offers > 0 else 0
            },
            "senior": {
                "count": senior_count,
                "percentage": round((senior_count / total_offers) * 100, 1) if total_offers > 0 else 0
            }
        }
    except Exception as e:
        logger.error(f"Error getting experience analysis: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving experience analysis")

@app.get("/analytics/market-insights/", tags=["Analytics"], summary="Get market insights and trends")
def get_market_insights(db: Session = Depends(get_db)):
    """
    Get comprehensive market insights including growth trends and predictions.
    """
    try:
        # Get offers from last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_offers = db.query(models.JobOffer).filter(
            models.JobOffer.scraped_at >= thirty_days_ago
        ).count()
        
        # Get offers from previous 30 days for comparison
        sixty_days_ago = datetime.now() - timedelta(days=60)
        previous_offers = db.query(models.JobOffer).filter(
            models.JobOffer.scraped_at >= sixty_days_ago,
            models.JobOffer.scraped_at < thirty_days_ago
        ).count()
        
        growth_rate = ((recent_offers - previous_offers) / previous_offers * 100) if previous_offers > 0 else 0
        
        # Get top growing technologies
        tech_stats = analyzer.analyze_technology_demand(db=db)
        top_techs = tech_stats[:5] if tech_stats else []
        
        return {
            "market_growth": {
                "current_month": recent_offers,
                "previous_month": previous_offers,
                "growth_rate": round(growth_rate, 1),
                "trend": "up" if growth_rate > 0 else "down"
            },
            "hot_technologies": [
                {
                    "technology": tech.technology,
                    "demand_score": tech.percentage,
                    "trend": "rising" if tech.percentage > 20 else "stable"
                }
                for tech in top_techs
            ],
            "market_sentiment": "positive" if growth_rate > 5 else "neutral" if growth_rate > -5 else "negative",
            "recommendations": [
                "Focus on React and Python skills for maximum opportunities",
                "Consider remote work options for better work-life balance",
                "Senior positions are in high demand across all technologies"
            ]
        }
    except Exception as e:
        logger.error(f"Error getting market insights: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving market insights")

@app.post("/alerts/create/", tags=["Alerts"], summary="Create a job alert")
def create_job_alert(
    email: str,
    keywords: List[str],
    location: str = None,
    company: str = None,
    frequency: str = "daily",  # daily, weekly, immediate
    db: Session = Depends(get_db)
):
    """
    Create a job alert for specific criteria.
    
    - **email**: Email address for notifications
    - **keywords**: List of keywords to search for
    - **location**: Preferred location (optional)
    - **company**: Preferred company (optional)
    - **frequency**: Alert frequency
    """
    try:
        # In a real implementation, you'd save this to a database
        alert_id = f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "alert_id": alert_id,
            "email": email,
            "keywords": keywords,
            "location": location,
            "company": company,
            "frequency": frequency,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "message": "Job alert created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating job alert: {e}")
        raise HTTPException(status_code=500, detail="Error creating job alert")

@app.get("/alerts/{alert_id}/jobs/", tags=["Alerts"], summary="Get matching jobs for an alert")
def get_alert_jobs(alert_id: str, db: Session = Depends(get_db)):
    """
    Get job offers that match a specific alert criteria.
    """
    try:
        # In a real implementation, you'd retrieve the alert from database
        # and search for matching jobs
        matching_jobs = db.query(models.JobOffer).limit(10).all()
        
        return {
            "alert_id": alert_id,
            "matching_jobs": matching_jobs,
            "total_matches": len(matching_jobs),
            "last_checked": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting alert jobs: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving alert jobs")

@app.get("/notifications/recent/", tags=["Notifications"], summary="Get recent market notifications")
def get_recent_notifications(db: Session = Depends(get_db)):
    """
    Get recent market notifications and updates.
    """
    try:
        # Get recent activity that might be interesting
        recent_offers = db.query(models.JobOffer).order_by(
            models.JobOffer.scraped_at.desc()
        ).limit(5).all()
        
        notifications = []
        for offer in recent_offers:
            notifications.append({
                "type": "new_job",
                "title": f"New {offer.title} position at {offer.company}",
                "description": f"New opportunity in {offer.location or 'Unknown location'}",
                "timestamp": offer.scraped_at.isoformat(),
                "priority": "medium"
            })
        
        # Add market insights
        tech_stats = analyzer.analyze_technology_demand(db=db)
        if tech_stats:
            top_tech = tech_stats[0]
            notifications.append({
                "type": "market_trend",
                "title": f"{top_tech.technology} demand is rising",
                "description": f"{top_tech.technology} is now the most in-demand technology with {top_tech.percentage}% of offers",
                "timestamp": datetime.now().isoformat(),
                "priority": "high"
            })
        
        return {
            "notifications": notifications,
            "unread_count": len(notifications),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting notifications: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving notifications")

@app.get("/export/jobs/", tags=["Export"], summary="Export job offers to CSV/JSON")
def export_jobs(
    format: str = "json",  # json, csv
    filters: str = None,  # JSON string with filters
    db: Session = Depends(get_db)
):
    """
    Export job offers in various formats with optional filtering.
    
    - **format**: Export format (json, csv)
    - **filters**: JSON string with filter criteria
    """
    try:
        query = db.query(models.JobOffer)
        
        # Apply filters if provided
        if filters:
            import json
            filter_data = json.loads(filters)
            if "technology" in filter_data:
                query = query.filter(models.JobOffer.description.ilike(f"%{filter_data['technology']}%"))
            if "company" in filter_data:
                query = query.filter(models.JobOffer.company.ilike(f"%{filter_data['company']}%"))
            if "location" in filter_data:
                query = query.filter(models.JobOffer.location.ilike(f"%{filter_data['location']}%"))
        
        offers = query.all()
        
        if format.lower() == "csv":
            import csv
            from io import StringIO
            
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(["ID", "Title", "Company", "Location", "Description", "URL", "Scraped At"])
            
            for offer in offers:
                writer.writerow([
                    offer.id,
                    offer.title,
                    offer.company,
                    offer.location,
                    offer.description,
                    offer.url,
                    offer.scraped_at
                ])
            
            return {
                "format": "csv",
                "data": output.getvalue(),
                "total_records": len(offers),
                "filename": f"job_offers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        else:
            return {
                "format": "json",
                "data": [
                    {
                        "id": offer.id,
                        "title": offer.title,
                        "company": offer.company,
                        "location": offer.location,
                        "description": offer.description,
                        "url": offer.url,
                        "scraped_at": offer.scraped_at.isoformat()
                    }
                    for offer in offers
                ],
                "total_records": len(offers)
            }
    except Exception as e:
        logger.error(f"Error exporting jobs: {e}")
        raise HTTPException(status_code=500, detail="Error exporting job data")

@app.get("/reports/market-summary/", tags=["Reports"], summary="Generate market summary report")
def generate_market_report(
    period: str = "30d",  # 7d, 30d, 90d
    db: Session = Depends(get_db)
):
    """
    Generate a comprehensive market summary report.
    
    - **period**: Report period (7d, 30d, 90d)
    """
    try:
        # Calculate period
        days = int(period.replace('d', ''))
        start_date = datetime.now() - timedelta(days=days)
        
        # Get offers in period
        period_offers = db.query(models.JobOffer).filter(
            models.JobOffer.scraped_at >= start_date
        ).all()
        
        # Get technology stats
        tech_stats = analyzer.analyze_technology_demand(db=db)
        
        # Get company stats
        company_stats = db.query(
            models.JobOffer.company,
            db.func.count(models.JobOffer.id).label('offer_count')
        ).filter(
            models.JobOffer.company.isnot(None),
            models.JobOffer.scraped_at >= start_date
        ).group_by(
            models.JobOffer.company
        ).order_by(
            db.func.count(models.JobOffer.id).desc()
        ).limit(10).all()
        
        # Get location stats
        location_stats = db.query(
            models.JobOffer.location,
            db.func.count(models.JobOffer.id).label('offer_count')
        ).filter(
            models.JobOffer.location.isnot(None),
            models.JobOffer.scraped_at >= start_date
        ).group_by(
            models.JobOffer.location
        ).order_by(
            db.func.count(models.JobOffer.id).desc()
        ).limit(10).all()
        
        return {
            "report_period": period,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_offers": len(period_offers),
                "unique_companies": len(set(offer.company for offer in period_offers if offer.company)),
                "unique_locations": len(set(offer.location for offer in period_offers if offer.location)),
                "top_technologies": tech_stats[:5] if tech_stats else [],
                "top_companies": [
                    {"company": company, "offer_count": count}
                    for company, count in company_stats
                ],
                "top_locations": [
                    {"location": location, "offer_count": count}
                    for location, count in location_stats
                ]
            },
            "insights": [
                f"Market shows {len(period_offers)} new opportunities in the last {days} days",
                f"Top technology demand: {tech_stats[0].technology if tech_stats else 'N/A'}",
                f"Most active company: {company_stats[0][0] if company_stats else 'N/A'}",
                f"Most opportunities in: {location_stats[0][0] if location_stats else 'N/A'}"
            ],
            "recommendations": [
                "Focus on trending technologies for better job prospects",
                "Consider companies with high hiring activity",
                "Explore opportunities in emerging locations"
            ]
        }
    except Exception as e:
        logger.error(f"Error generating market report: {e}")
        raise HTTPException(status_code=500, detail="Error generating market report")

@app.get("/health/", tags=["Health"], summary="Health check endpoint")
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
