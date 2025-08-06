import os
from typing import List

class Settings:
    """Application settings and configuration."""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:2024@localhost:3306/job_market")
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Scraping settings
    BASE_URL: str = os.getenv("BASE_URL", "https://www.computrabajo.com.co/ofertas-de-trabajo/?q=python")
    MAX_PAGES: int = int(os.getenv("MAX_PAGES", "10"))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "15"))
    RETRY_ATTEMPTS: int = int(os.getenv("RETRY_ATTEMPTS", "3"))
    DELAY_BETWEEN_REQUESTS: float = float(os.getenv("DELAY_BETWEEN_REQUESTS", "1.0"))
    
    # Headers for web scraping
    HEADERS: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Technologies to analyze
    TECHNOLOGIES: List[str] = [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C#', 'C++', 'PHP', 'Ruby', 'Go', 'Swift', 'Kotlin',
        'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'Spring', 'ASP.NET',
        'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis',
        'AWS', 'Azure', 'Google Cloud', 'GCP', 'Docker', 'Kubernetes',
        'Git', 'Jenkins', 'Terraform'
    ]

settings = Settings() 