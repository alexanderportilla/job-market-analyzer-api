#!/usr/bin/env python3

import sys
import os
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, get_db
from app import models

def create_test_data():
    """Create test job offers data"""
    print("Creating test data...")
    
    # Sample job offers data
    test_offers = [
        {
            "title": "Senior Python Developer",
            "company": "TechCorp Colombia",
            "location": "Bogotá, Colombia",
            "description": "Buscamos un desarrollador Python senior con experiencia en Django, React y PostgreSQL. Debe tener al menos 5 años de experiencia en desarrollo web.",
            "url": "https://example.com/job1",
            "source": "computrabajo"
        },
        {
            "title": "Full Stack React Developer",
            "company": "StartupXYZ",
            "location": "Medellín, Colombia",
            "description": "Desarrollador full stack con experiencia en React, Node.js, TypeScript y MongoDB. Conocimientos en Docker y AWS serán valorados.",
            "url": "https://example.com/job2",
            "source": "computrabajo"
        },
        {
            "title": "Frontend Engineer",
            "company": "BigTech Inc",
            "location": "Cali, Colombia",
            "description": "Ingeniero frontend especializado en React, Vue.js y TypeScript. Experiencia con Redux, GraphQL y testing con Jest.",
            "url": "https://example.com/job3",
            "source": "computrabajo"
        },
        {
            "title": "Java Backend Developer",
            "company": "Enterprise Solutions",
            "location": "Barranquilla, Colombia",
            "description": "Desarrollador Java con experiencia en Spring Boot, Hibernate, MySQL. Conocimientos en microservicios y Docker.",
            "url": "https://example.com/job4",
            "source": "computrabajo"
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudTech",
            "location": "Bogotá, Colombia",
            "description": "Ingeniero DevOps con experiencia en AWS, Docker, Kubernetes, Jenkins y Terraform. Conocimientos en Python y bash scripting.",
            "url": "https://example.com/job5",
            "source": "computrabajo"
        },
        {
            "title": "Data Scientist",
            "company": "Analytics Pro",
            "location": "Medellín, Colombia",
            "description": "Científico de datos con experiencia en Python, pandas, scikit-learn, TensorFlow y SQL. Conocimientos en machine learning y estadística.",
            "url": "https://example.com/job6",
            "source": "computrabajo"
        },
        {
            "title": "Mobile Developer (React Native)",
            "company": "AppStudio",
            "location": "Cali, Colombia",
            "description": "Desarrollador móvil con experiencia en React Native, JavaScript, TypeScript. Conocimientos en Firebase y APIs REST.",
            "url": "https://example.com/job7",
            "source": "computrabajo"
        },
        {
            "title": "QA Automation Engineer",
            "company": "Quality First",
            "location": "Bogotá, Colombia",
            "description": "Ingeniero QA con experiencia en Selenium, Cypress, Python y JavaScript. Conocimientos en testing de APIs y CI/CD.",
            "url": "https://example.com/job8",
            "source": "computrabajo"
        },
        {
            "title": "Product Manager",
            "company": "Innovation Lab",
            "location": "Medellín, Colombia",
            "description": "Product Manager con experiencia en metodologías ágiles, Jira, Confluence. Conocimientos técnicos en desarrollo web y móvil.",
            "url": "https://example.com/job9",
            "source": "computrabajo"
        },
        {
            "title": "UX/UI Designer",
            "company": "Design Studio",
            "location": "Bogotá, Colombia",
            "description": "Diseñador UX/UI con experiencia en Figma, Adobe Creative Suite, HTML, CSS. Conocimientos en investigación de usuarios.",
            "url": "https://example.com/job10",
            "source": "computrabajo"
        }
    ]
    
    # Create database session
    db = next(get_db())
    
    try:
        # Add offers with different timestamps to simulate real data
        for i, offer_data in enumerate(test_offers):
            # Create different timestamps (some recent, some older)
            if i < 3:
                # Recent offers (last 7 days)
                scraped_at = datetime.now() - timedelta(days=i+1)
            elif i < 7:
                # Medium age offers (last 30 days)
                scraped_at = datetime.now() - timedelta(days=15+i)
            else:
                # Older offers (last 90 days)
                scraped_at = datetime.now() - timedelta(days=60+i)
            
            offer = models.JobOffer(
                title=offer_data["title"],
                company=offer_data["company"],
                location=offer_data["location"],
                description=offer_data["description"],
                url=offer_data["url"],
                source=offer_data["source"],
                scraped_at=scraped_at
            )
            
            db.add(offer)
        
        # Commit the changes
        db.commit()
        print(f"✅ Successfully created {len(test_offers)} test job offers")
        
        # Verify the data was created
        total_offers = db.query(models.JobOffer).count()
        print(f"📊 Total offers in database: {total_offers}")
        
        # Show some statistics
        companies = db.query(models.JobOffer.company).distinct().count()
        locations = db.query(models.JobOffer.location).distinct().count()
        print(f"🏢 Unique companies: {companies}")
        print(f"📍 Unique locations: {locations}")
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data() 