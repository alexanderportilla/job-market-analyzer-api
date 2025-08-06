#!/usr/bin/env python3
"""
Setup script for MySQL Workbench configuration
"""
import os
import sys
import subprocess
import mysql.connector
from mysql.connector import Error

def create_database():
    """Create the job_market database if it doesn't exist."""
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2024"  # Updated password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS job_market")
            print("✅ Database 'job_market' created successfully")
            
            # Use the database
            cursor.execute("USE job_market")
            print("✅ Using database 'job_market'")
            
            # Create tables (this will be done by SQLAlchemy, but we can verify)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_offers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    company VARCHAR(255),
                    location VARCHAR(255),
                    description TEXT,
                    url VARCHAR(500) UNIQUE,
                    source VARCHAR(100),
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_title (title),
                    INDEX idx_company (company)
                )
            """)
            print("✅ Table 'job_offers' created successfully")
            
            cursor.close()
            connection.close()
            print("✅ MySQL connection closed")
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("\n📋 Please make sure:")
        print("1. MySQL Server is installed and running")
        print("2. MySQL Workbench is installed")
        print("3. Root password is set correctly")
        print("4. MySQL service is running on port 3306")
        return False
    
    return True

def check_mysql_connection():
    """Check if MySQL is accessible."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2024"  # Updated password
        )
        
        if connection.is_connected():
            print("✅ MySQL connection successful")
            connection.close()
            return True
    except Error as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up MySQL Workbench for Job Market Analyzer API...")
    
    # Check MySQL connection
    if not check_mysql_connection():
        print("\n📋 MySQL Setup Instructions:")
        print("1. Download and install MySQL Server from: https://dev.mysql.com/downloads/mysql/")
        print("2. Download and install MySQL Workbench from: https://dev.mysql.com/downloads/workbench/")
        print("3. Set root password during installation")
        print("4. Start MySQL service")
        print("5. Update the password in this script if different from 'password'")
        print("6. Run this script again")
        return
    
    # Create database and tables
    if create_database():
        print("\n✅ MySQL setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Open MySQL Workbench")
        print("2. Connect to localhost:3306 with root user")
        print("3. You should see the 'job_market' database")
        print("4. Run the application:")
        print("   uvicorn app.main:app --reload")
        print("5. The tables will be created automatically when you first run the app")
    else:
        print("❌ MySQL setup failed")

if __name__ == "__main__":
    main() 