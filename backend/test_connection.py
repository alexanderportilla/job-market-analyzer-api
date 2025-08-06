#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("Testing imports...")
        from app import models, schemas, scraper, analyzer
        from app.database import engine, get_db
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_database():
    """Test database connection"""
    try:
        print("Testing database connection...")
        from app.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_fastapi():
    """Test FastAPI app creation"""
    try:
        print("Testing FastAPI app...")
        from app.main import app
        print("✅ FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"❌ FastAPI error: {e}")
        return False

if __name__ == "__main__":
    print("=== Job Market Analyzer API Test ===")
    
    success = True
    success &= test_imports()
    success &= test_database()
    success &= test_fastapi()
    
    if success:
        print("\n🎉 All tests passed! The API should work correctly.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1) 