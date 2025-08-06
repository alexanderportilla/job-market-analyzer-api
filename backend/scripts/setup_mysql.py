#!/usr/bin/env python3
"""
MySQL Database Setup Script for Job Market Analyzer
This script sets up the MySQL database and provides functions to save scraped data.
"""

import mysql.connector
from mysql.connector import Error
import os
import sys
import logging
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Base
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MySQLManager:
    """Manages MySQL database operations for the Job Market Analyzer."""
    
    def __init__(self):
        self.connection = None
        self.engine = None
        self.SessionLocal = None
        
    def connect_mysql(self):
        """Establish connection to MySQL server."""
        try:
            # Parse database URL to get connection details
            db_url = settings.DATABASE_URL
            # mysql+mysqlconnector://root:2024@localhost:3306/job_market
            parts = db_url.replace('mysql+mysqlconnector://', '').split('@')
            user_pass = parts[0].split(':')
            host_db = parts[1].split('/')
            
            username = user_pass[0]
            password = user_pass[1]
            host = host_db[0].split(':')[0]
            port = int(host_db[0].split(':')[1]) if ':' in host_db[0] else 3306
            database = host_db[1]
            
            # Connect to MySQL server (without database first)
            self.connection = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password
            )
            
            logger.info("✅ Successfully connected to MySQL server")
            return True
            
        except Error as e:
            logger.error(f"❌ Error connecting to MySQL: {e}")
            return False
    
    def create_database(self):
        """Create the job_market database if it doesn't exist."""
        try:
            cursor = self.connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS job_market")
            logger.info("✅ Database 'job_market' created or already exists")
            
            # Use the database
            cursor.execute("USE job_market")
            logger.info("✅ Using database 'job_market'")
            
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"❌ Error creating database: {e}")
            return False
    
    def create_tables(self):
        """Create all tables using SQLAlchemy."""
        try:
            # Create engine with the specific database
            self.engine = create_engine(
                settings.DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=False
            )
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            logger.info("✅ All tables created successfully")
            
            # Create session factory
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error creating tables: {e}")
            return False
    
    def verify_tables(self):
        """Verify that all tables exist and have the correct structure."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("USE job_market")
            
            # Check if tables exist
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            
            expected_tables = ['users', 'job_offers', 'job_alerts', 'saved_jobs']
            
            for table in expected_tables:
                if table in tables:
                    logger.info(f"✅ Table '{table}' exists")
                else:
                    logger.warning(f"⚠️ Table '{table}' is missing")
            
            # Check table structures
            for table in expected_tables:
                if table in tables:
                    cursor.execute(f"DESCRIBE {table}")
                    columns = cursor.fetchall()
                    logger.info(f"📋 Table '{table}' has {len(columns)} columns")
            
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"❌ Error verifying tables: {e}")
            return False
    
    def insert_sample_data(self):
        """Insert sample data for testing."""
        try:
            from app.models import JobOffer, User, JobAlert, SavedJob
            
            session = self.SessionLocal()
            
            # Sample job offers
            sample_offers = [
                {
                    "title": "Python Developer",
                    "company": "TechCorp",
                    "location": "Bogotá",
                    "description": "We are looking for a Python developer with Django experience",
                    "url": "https://example.com/job1",
                    "source": "Computrabajo"
                },
                {
                    "title": "React Developer",
                    "company": "StartupXYZ",
                    "location": "Medellín",
                    "description": "Frontend developer with React and TypeScript skills",
                    "url": "https://example.com/job2",
                    "source": "Computrabajo"
                },
                {
                    "title": "Full Stack Developer",
                    "company": "InnovationLab",
                    "location": "Cali",
                    "description": "Full stack developer with Python and React experience",
                    "url": "https://example.com/job3",
                    "source": "Computrabajo"
                }
            ]
            
            for offer_data in sample_offers:
                # Check if offer already exists
                existing = session.query(JobOffer).filter(JobOffer.url == offer_data["url"]).first()
                if not existing:
                    offer = JobOffer(**offer_data)
                    session.add(offer)
                    logger.info(f"✅ Added sample job offer: {offer_data['title']}")
            
            session.commit()
            session.close()
            logger.info("✅ Sample data inserted successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error inserting sample data: {e}")
            return False
    
    def save_scraped_data(self, job_data_list):
        """Save scraped job data to MySQL database."""
        try:
            from app.models import JobOffer
            
            session = self.SessionLocal()
            saved_count = 0
            
            for job_data in job_data_list:
                # Check if job already exists
                existing = session.query(JobOffer).filter(JobOffer.url == job_data["url"]).first()
                
                if not existing:
                    job_offer = JobOffer(**job_data)
                    session.add(job_offer)
                    saved_count += 1
                    logger.info(f"💾 Saved job: {job_data['title']} at {job_data['company']}")
                else:
                    logger.info(f"⏭️ Job already exists: {job_data['title']}")
            
            session.commit()
            session.close()
            
            logger.info(f"✅ Successfully saved {saved_count} new job offers to MySQL")
            return saved_count
            
        except Exception as e:
            logger.error(f"❌ Error saving scraped data: {e}")
            return 0
    
    def get_database_stats(self):
        """Get statistics about the database."""
        try:
            session = self.SessionLocal()
            
            from app.models import JobOffer, User, JobAlert, SavedJob
            
            stats = {
                "total_job_offers": session.query(JobOffer).count(),
                "total_users": session.query(User).count(),
                "total_alerts": session.query(JobAlert).count(),
                "total_saved_jobs": session.query(SavedJob).count(),
                "recent_offers": session.query(JobOffer).filter(
                    JobOffer.scraped_at >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                ).count()
            }
            
            session.close()
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error getting database stats: {e}")
            return {}
    
    def close_connection(self):
        """Close the MySQL connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("✅ MySQL connection closed")

def setup_mysql_database():
    """Main function to set up the MySQL database."""
    mysql_manager = MySQLManager()
    
    try:
        logger.info("🚀 Starting MySQL database setup...")
        
        # Step 1: Connect to MySQL
        if not mysql_manager.connect_mysql():
            logger.error("❌ Failed to connect to MySQL. Please check your MySQL server and credentials.")
            return False
        
        # Step 2: Create database
        if not mysql_manager.create_database():
            logger.error("❌ Failed to create database.")
            return False
        
        # Step 3: Create tables
        if not mysql_manager.create_tables():
            logger.error("❌ Failed to create tables.")
            return False
        
        # Step 4: Verify tables
        if not mysql_manager.verify_tables():
            logger.error("❌ Failed to verify tables.")
            return False
        
        # Step 5: Insert sample data (optional)
        insert_sample = input("Do you want to insert sample data? (y/n): ").lower().strip()
        if insert_sample == 'y':
            mysql_manager.insert_sample_data()
        
        # Step 6: Show database stats
        stats = mysql_manager.get_database_stats()
        logger.info("📊 Database Statistics:")
        for key, value in stats.items():
            logger.info(f"   {key}: {value}")
        
        logger.info("🎉 MySQL database setup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Setup failed: {e}")
        return False
    
    finally:
        mysql_manager.close_connection()

def test_mysql_connection():
    """Test the MySQL connection and configuration."""
    mysql_manager = MySQLManager()
    
    try:
        logger.info("🔍 Testing MySQL connection...")
        
        if mysql_manager.connect_mysql():
            logger.info("✅ MySQL connection test successful")
            
            # Test database access
            cursor = mysql_manager.connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if 'job_market' in databases:
                logger.info("✅ Database 'job_market' exists")
                
                # Test table access
                cursor.execute("USE job_market")
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                logger.info(f"✅ Found {len(tables)} tables: {', '.join(tables)}")
            else:
                logger.warning("⚠️ Database 'job_market' does not exist")
            
            cursor.close()
            return True
        else:
            logger.error("❌ MySQL connection test failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Connection test failed: {e}")
        return False
    
    finally:
        mysql_manager.close_connection()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MySQL Database Setup for Job Market Analyzer")
    parser.add_argument("--test", action="store_true", help="Test MySQL connection only")
    parser.add_argument("--setup", action="store_true", help="Setup MySQL database")
    
    args = parser.parse_args()
    
    if args.test:
        test_mysql_connection()
    elif args.setup:
        setup_mysql_database()
    else:
        # Default: run setup
        setup_mysql_database() 