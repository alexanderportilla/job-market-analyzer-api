-- MySQL Configuration for Job Market Analyzer API
-- Run this in MySQL Workbench to set up the database

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS job_market;

-- Use the database
USE job_market;

-- Create the job_offers table
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
    INDEX idx_company (company),
    INDEX idx_scraped_at (scraped_at)
);

-- Create a user for the application (optional)
-- CREATE USER IF NOT EXISTS 'appuser'@'localhost' IDENTIFIED BY 'apppassword';
-- GRANT ALL PRIVILEGES ON job_market.* TO 'appuser'@'localhost';
-- FLUSH PRIVILEGES;

-- Show the created table structure
DESCRIBE job_offers;

-- Show sample data (will be empty initially)
SELECT * FROM job_offers LIMIT 5; 