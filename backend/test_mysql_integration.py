#!/usr/bin/env python3
"""
MySQL Integration Test Script
Tests the complete MySQL integration for the Job Market Analyzer.
"""

import sys
import os
import logging
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import get_db, engine
from app.models import Base, JobOffer
from app.scraper import scrape_job_offers, get_database_stats, save_job_offers_to_mysql
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_mysql_connection():
    """Test MySQL connection and basic operations."""
    logger.info("🔍 Testing MySQL connection...")
    
    try:
        # Test database connection
        db = next(get_db())
        logger.info("✅ Database connection successful")
        
        # Test table creation
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables created/verified successfully")
        
        db.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ MySQL connection test failed: {e}")
        return False

def test_data_insertion():
    """Test inserting sample data into MySQL."""
    logger.info("💾 Testing data insertion...")
    
    try:
        db = next(get_db())
        
        # Sample job data
        sample_jobs = [
            {
                "title": "Python Developer",
                "company": "TechCorp Colombia",
                "location": "Bogotá",
                "description": "We are looking for a Python developer with Django and Flask experience",
                "url": "https://example.com/job1",
                "source": "Computrabajo"
            },
            {
                "title": "React Developer",
                "company": "StartupXYZ",
                "location": "Medellín",
                "description": "Frontend developer with React, TypeScript, and Redux skills",
                "url": "https://example.com/job2",
                "source": "Computrabajo"
            },
            {
                "title": "Full Stack Developer",
                "company": "InnovationLab",
                "location": "Cali",
                "description": "Full stack developer with Python, React, and PostgreSQL experience",
                "url": "https://example.com/job3",
                "source": "Computrabajo"
            }
        ]
        
        # Save sample data
        saved_count = save_job_offers_to_mysql(sample_jobs, db)
        
        if saved_count > 0:
            logger.info(f"✅ Successfully inserted {saved_count} sample job offers")
            
            # Get database stats
            stats = get_database_stats(db)
            logger.info("📊 Database Statistics:")
            for key, value in stats.items():
                logger.info(f"   {key}: {value}")
            
            return True
        else:
            logger.warning("⚠️ No new data was inserted (might already exist)")
            return True
            
    except Exception as e:
        logger.error(f"❌ Data insertion test failed: {e}")
        return False
    finally:
        db.close()

def test_scraping_integration():
    """Test the complete scraping and MySQL integration."""
    logger.info("🚀 Testing complete scraping integration...")
    
    try:
        db = next(get_db())
        
        # Test scraping with 1 page
        result = scrape_job_offers(db, pages=1)
        
        logger.info(f"✅ Scraping test completed: {result}")
        
        # Get updated stats
        stats = get_database_stats(db)
        logger.info("📊 Updated Database Statistics:")
        for key, value in stats.items():
            logger.info(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Scraping integration test failed: {e}")
        return False
    finally:
        db.close()

def test_database_operations():
    """Test various database operations."""
    logger.info("🔧 Testing database operations...")
    
    try:
        db = next(get_db())
        
        # Test querying job offers
        total_offers = db.query(JobOffer).count()
        logger.info(f"📋 Total job offers in database: {total_offers}")
        
        # Test querying by company
        companies = db.query(JobOffer.company).distinct().all()
        logger.info(f"🏢 Unique companies: {len(companies)}")
        
        # Test querying recent offers
        from datetime import datetime, timedelta
        yesterday = datetime.now() - timedelta(days=1)
        recent_offers = db.query(JobOffer).filter(JobOffer.scraped_at >= yesterday).count()
        logger.info(f"🕒 Recent offers (last 24h): {recent_offers}")
        
        # Test querying by location
        locations = db.query(JobOffer.location).distinct().all()
        logger.info(f"📍 Unique locations: {len(locations)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database operations test failed: {e}")
        return False
    finally:
        db.close()

def run_complete_test():
    """Run all tests in sequence."""
    logger.info("🧪 Starting MySQL Integration Tests...")
    logger.info("=" * 50)
    
    tests = [
        ("MySQL Connection", test_mysql_connection),
        ("Data Insertion", test_data_insertion),
        ("Database Operations", test_database_operations),
        ("Scraping Integration", test_scraping_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n🔍 Running: {test_name}")
        logger.info("-" * 30)
        
        try:
            if test_func():
                logger.info(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                logger.error(f"❌ {test_name}: FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name}: ERROR - {e}")
    
    logger.info("\n" + "=" * 50)
    logger.info(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! MySQL integration is working correctly.")
        return True
    else:
        logger.error(f"⚠️ {total - passed} test(s) failed. Please check the configuration.")
        return False

def show_database_info():
    """Show current database configuration and status."""
    logger.info("📋 Database Configuration:")
    logger.info(f"   Database URL: {settings.DATABASE_URL}")
    logger.info(f"   API Host: {settings.API_HOST}")
    logger.info(f"   API Port: {settings.API_PORT}")
    logger.info(f"   Environment: {settings.ENVIRONMENT}")
    
    try:
        db = next(get_db())
        stats = get_database_stats(db)
        db.close()
        
        logger.info("\n📊 Current Database Status:")
        for key, value in stats.items():
            logger.info(f"   {key}: {value}")
            
    except Exception as e:
        logger.error(f"❌ Could not retrieve database status: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MySQL Integration Test for Job Market Analyzer")
    parser.add_argument("--info", action="store_true", help="Show database information only")
    parser.add_argument("--connection", action="store_true", help="Test connection only")
    parser.add_argument("--insert", action="store_true", help="Test data insertion only")
    parser.add_argument("--scraping", action="store_true", help="Test scraping integration only")
    parser.add_argument("--operations", action="store_true", help="Test database operations only")
    
    args = parser.parse_args()
    
    if args.info:
        show_database_info()
    elif args.connection:
        test_mysql_connection()
    elif args.insert:
        test_data_insertion()
    elif args.scraping:
        test_scraping_integration()
    elif args.operations:
        test_database_operations()
    else:
        # Run complete test suite
        run_complete_test() 