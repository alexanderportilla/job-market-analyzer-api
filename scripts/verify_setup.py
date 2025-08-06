#!/usr/bin/env python3
"""
Verification script to ensure all components are properly synchronized
"""
import os
import sys
import subprocess
import mysql.connector
from pathlib import Path

def check_python_dependencies():
    """Check if all Python dependencies are installed."""
    print("🔍 Checking Python dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'sqlalchemy', 'pandas', 
        'bs4', 'requests', 'mysql.connector'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r backend/requirements.txt")
        return False
    
    print("✅ All Python dependencies are installed")
    return True

def check_mysql_connection():
    """Check MySQL connection and database."""
    print("\n🔍 Checking MySQL connection...")
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2024",
            database="job_market"
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check if table exists
            cursor.execute("SHOW TABLES LIKE 'job_offers'")
            if cursor.fetchone():
                print("✅ Database 'job_market' exists")
                print("✅ Table 'job_offers' exists")
                
                # Check table structure
                cursor.execute("DESCRIBE job_offers")
                columns = cursor.fetchall()
                print(f"✅ Table has {len(columns)} columns")
                
            else:
                print("❌ Table 'job_offers' not found")
                print("Run: python backend/scripts/setup_mysql.py")
                cursor.close()
                connection.close()
                return False
            
            cursor.close()
            connection.close()
            print("✅ MySQL connection successful")
            return True
            
    except mysql.connector.Error as e:
        print(f"❌ MySQL connection failed: {e}")
        print("Make sure MySQL is running and password is correct")
        return False

def check_file_structure():
    """Check if all required files exist."""
    print("\n🔍 Checking file structure...")
    
    required_files = [
        'backend/app/main.py',
        'backend/app/config.py',
        'backend/app/database.py',
        'backend/app/models.py',
        'backend/app/schemas.py',
        'backend/app/scraper.py',
        'backend/app/analyzer.py',
        'backend/requirements.txt',
        'backend/scripts/setup_mysql.py',
        'frontend/package.json',
        'frontend/src/App.tsx',
        'frontend/src/main.tsx',
        'docker-compose.yml'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path} - MISSING")
    
    if missing_files:
        print(f"\n⚠️  Missing files: {len(missing_files)}")
        return False
    
    print("✅ All required files exist")
    return True

def check_configuration():
    """Check configuration consistency."""
    print("\n🔍 Checking configuration consistency...")
    
    # Read config.py
    config_path = Path('backend/app/config.py')
    if config_path.exists():
        with open(config_path, 'r') as f:
            config_content = f.read()
            
        if 'mysql+mysqlconnector://root:2024@localhost:3306/job_market' in config_content:
            print("✅ Database URL configured correctly")
        else:
            print("❌ Database URL not configured correctly")
            return False
            
        if 'job_market' in config_content:
            print("✅ Database name configured correctly")
        else:
            print("❌ Database name not configured correctly")
            return False
    else:
        print("❌ config.py not found")
        return False
    
    # Check docker-compose.yml
    docker_path = Path('docker-compose.yml')
    if docker_path.exists():
        with open(docker_path, 'r') as f:
            docker_content = f.read()
            
        if 'mysql+mysqlconnector://root:2024@db:3306/job_market' in docker_content:
            print("✅ Docker database URL configured correctly")
        else:
            print("❌ Docker database URL not configured correctly")
            return False
            
        if 'MYSQL_ROOT_PASSWORD=2024' in docker_content:
            print("✅ Docker MySQL password configured correctly")
        else:
            print("❌ Docker MySQL password not configured correctly")
            return False
    else:
        print("❌ docker-compose.yml not found")
        return False
    
    print("✅ Configuration is consistent")
    return True

def main():
    """Main verification function."""
    print("🚀 Job Market Analyzer - Setup Verification")
    print("=" * 50)
    
    checks = [
        check_file_structure,
        check_python_dependencies,
        check_mysql_connection,
        check_configuration
    ]
    
    all_passed = True
    
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Your setup is ready.")
        print("\n📋 Next steps:")
        print("1. Start backend: cd backend && uvicorn app.main:app --reload --port 8000")
        print("2. Start frontend: cd frontend && npm start")
        print("3. Or use Docker: docker-compose up --build")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\n📋 Common fixes:")
        print("1. Install dependencies: pip install -r backend/requirements.txt")
        print("2. Setup MySQL: python backend/scripts/setup_mysql.py")
        print("3. Check MySQL is running and password is correct")

if __name__ == "__main__":
    main() 