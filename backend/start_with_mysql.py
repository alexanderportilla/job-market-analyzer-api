#!/usr/bin/env python3
"""
Startup Script for Job Market Analyzer with MySQL Integration
This script sets up MySQL, tests the connection, and starts the application.
"""

import os
import sys
import subprocess
import logging
import time
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_mysql_installation():
    """Check if MySQL is installed and running."""
    logger.info("🔍 Checking MySQL installation...")
    
    try:
        # Check if MySQL service is running
        result = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ MySQL is installed")
            return True
        else:
            logger.error("❌ MySQL is not installed or not in PATH")
            return False
    except FileNotFoundError:
        logger.error("❌ MySQL command not found. Please install MySQL first.")
        return False

def check_mysql_connection():
    """Check if we can connect to MySQL server."""
    logger.info("🔍 Testing MySQL connection...")
    
    try:
        # Try to connect to MySQL
        result = subprocess.run([
            'mysql', '-u', 'root', '-p2024', '-e', 'SELECT 1;'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ MySQL connection successful")
            return True
        else:
            logger.error("❌ MySQL connection failed")
            logger.error(f"Error: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ MySQL connection error: {e}")
        return False

def setup_mysql_database():
    """Set up the MySQL database using our setup script."""
    logger.info("🚀 Setting up MySQL database...")
    
    try:
        # Run the MySQL setup script
        setup_script = Path(__file__).parent / "scripts" / "setup_mysql.py"
        
        if not setup_script.exists():
            logger.error(f"❌ Setup script not found: {setup_script}")
            return False
        
        result = subprocess.run([
            sys.executable, str(setup_script), "--setup"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ MySQL database setup completed")
            return True
        else:
            logger.error(f"❌ MySQL setup failed: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error running MySQL setup: {e}")
        return False

def test_mysql_integration():
    """Test the complete MySQL integration."""
    logger.info("🧪 Testing MySQL integration...")
    
    try:
        # Run the integration test
        test_script = Path(__file__).parent / "test_mysql_integration.py"
        
        if not test_script.exists():
            logger.error(f"❌ Test script not found: {test_script}")
            return False
        
        result = subprocess.run([
            sys.executable, str(test_script)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ MySQL integration test passed")
            return True
        else:
            logger.error(f"❌ MySQL integration test failed: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error running integration test: {e}")
        return False

def install_dependencies():
    """Install required Python dependencies."""
    logger.info("📦 Installing Python dependencies...")
    
    try:
        requirements_file = Path(__file__).parent / "requirements.txt"
        
        if not requirements_file.exists():
            logger.error(f"❌ Requirements file not found: {requirements_file}")
            return False
        
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ Dependencies installed successfully")
            return True
        else:
            logger.error(f"❌ Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error installing dependencies: {e}")
        return False

def start_application():
    """Start the FastAPI application."""
    logger.info("🚀 Starting Job Market Analyzer API...")
    
    try:
        # Change to the backend directory
        os.chdir(Path(__file__).parent)
        
        # Start the FastAPI application
        result = subprocess.run([
            sys.executable, "-m", "uvicorn", "app.main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ])
        
        return result.returncode == 0
        
    except KeyboardInterrupt:
        logger.info("⏹️ Application stopped by user")
        return True
    except Exception as e:
        logger.error(f"❌ Error starting application: {e}")
        return False

def show_instructions():
    """Show setup instructions if MySQL is not available."""
    logger.info("\n📋 MySQL Setup Instructions:")
    logger.info("1. Download MySQL Server from: https://dev.mysql.com/downloads/mysql/")
    logger.info("2. Install MySQL Server with default settings")
    logger.info("3. Set root password as '2024' during installation")
    logger.info("4. Download MySQL Workbench from: https://dev.mysql.com/downloads/workbench/")
    logger.info("5. Start MySQL service")
    logger.info("6. Run this script again")
    logger.info("\nAlternative: Use SQLite instead of MySQL by modifying app/config.py")

def main():
    """Main startup function."""
    logger.info("🎯 Job Market Analyzer - MySQL Startup")
    logger.info("=" * 50)
    
    # Step 1: Check MySQL installation
    if not check_mysql_installation():
        show_instructions()
        return False
    
    # Step 2: Check MySQL connection
    if not check_mysql_connection():
        logger.error("❌ Cannot connect to MySQL. Please check your MySQL server.")
        show_instructions()
        return False
    
    # Step 3: Install dependencies
    if not install_dependencies():
        logger.error("❌ Failed to install dependencies.")
        return False
    
    # Step 4: Setup MySQL database
    if not setup_mysql_database():
        logger.error("❌ Failed to setup MySQL database.")
        return False
    
    # Step 5: Test MySQL integration
    if not test_mysql_integration():
        logger.error("❌ MySQL integration test failed.")
        return False
    
    # Step 6: Start application
    logger.info("\n🎉 All checks passed! Starting application...")
    logger.info("📱 API will be available at: http://localhost:8000")
    logger.info("📚 API documentation at: http://localhost:8000/docs")
    logger.info("🔧 Press Ctrl+C to stop the application")
    logger.info("=" * 50)
    
    return start_application()

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1) 