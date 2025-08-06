#!/usr/bin/env python3

import sys
import os
import traceback

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_server():
    """Debug the server startup process"""
    try:
        print("=== Debugging Server Startup ===")
        
        # Test 1: Import modules
        print("1. Testing imports...")
        from app import models, schemas, scraper, analyzer
        from app.database import engine, get_db
        print("   ✅ Imports successful")
        
        # Test 2: Database connection
        print("2. Testing database connection...")
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("   ✅ Database connection successful")
        
        # Test 3: Create tables
        print("3. Testing table creation...")
        models.Base.metadata.create_all(bind=engine)
        print("   ✅ Tables created/verified")
        
        # Test 4: Create FastAPI app
        print("4. Testing FastAPI app creation...")
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        app = FastAPI(
            title="Job Market Analyzer API",
            description="An API to scrape and analyze job market data for software developers in Colombia.",
            version="1.0.0",
        )
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        print("   ✅ FastAPI app created successfully")
        
        # Test 5: Import the actual app
        print("5. Testing main app import...")
        from app.main import app as main_app
        print("   ✅ Main app imported successfully")
        
        print("\n🎉 All tests passed! Server should start correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during debugging: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_server()
    if not success:
        sys.exit(1) 