
import pandas as pd
from sqlalchemy.orm import Session
from . import models

# --- Data Analysis for Job Technologies ---

# A predefined list of technologies to search for.
# This list can be expanded or even moved to a configuration file.
TECHNOLOGIES = [
    'Python', 'Java', 'JavaScript', 'TypeScript', 'C#', 'C++', 'PHP', 'Ruby', 'Go', 'Swift', 'Kotlin',
    'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'Spring', 'ASP.NET',
    'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis',
    'AWS', 'Azure', 'Google Cloud', 'GCP', 'Docker', 'Kubernetes',
    'Git', 'Jenkins', 'Terraform'
]

def analyze_technology_demand(db: Session):
    """
    Analyzes the demand for technologies based on job descriptions in the database.

    Args:
        db: The database session.

    Returns:
        A list of dictionaries with technology and its count.
    """
    # Query all job offers from the database
    query = db.query(models.JobOffer.description).all()
    
    # Check if there is data to analyze
    if not query:
        return []

    # Use pandas for efficient text processing
    df = pd.DataFrame(query, columns=['description'])
    
    # Convert descriptions to lowercase for case-insensitive matching
    df['description_lower'] = df['description'].str.lower()

    results = []
    for tech in TECHNOLOGIES:
        # Use regex to find whole words to avoid matching substrings (e.g., 'Go' in 'Google')
        # The `\b` is a word boundary.
        tech_pattern = r'\b' + re.escape(tech.lower()) + r'\b'
        count = df['description_lower'].str.contains(tech_pattern, regex=True).sum()
        
        if count > 0:
            results.append({"technology": tech, "count": int(count)})

    # Sort results by count in descending order
    sorted_results = sorted(results, key=lambda x: x['count'], reverse=True)
    
    return sorted_results
