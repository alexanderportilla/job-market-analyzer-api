import pytest
from unittest.mock import Mock, patch
from app.analyzer import analyze_technology_demand
from app.models import JobOffer

class TestAnalyzer:
    """Test cases for the analyzer module."""
    
    def test_analyze_technology_demand_empty_db(self):
        """Test analysis with empty database."""
        mock_db = Mock()
        mock_db.query.return_value.all.return_value = []
        
        result = analyze_technology_demand(mock_db)
        assert result == []
    
    def test_analyze_technology_demand_with_data(self):
        """Test analysis with sample job data."""
        mock_db = Mock()
        mock_offer1 = Mock()
        mock_offer1.description = "We are looking for a Python developer with React experience"
        mock_offer2 = Mock()
        mock_offer2.description = "Java developer needed with Docker knowledge"
        
        mock_db.query.return_value.all.return_value = [mock_offer1, mock_offer2]
        
        result = analyze_technology_demand(mock_db)
        
        # Check that Python and Java are found
        python_count = next((item['count'] for item in result if item['technology'] == 'Python'), 0)
        java_count = next((item['count'] for item in result if item['technology'] == 'Java'), 0)
        
        assert python_count >= 1
        assert java_count >= 1
    
    def test_analyze_technology_demand_case_insensitive(self):
        """Test that technology matching is case insensitive."""
        mock_db = Mock()
        mock_offer = Mock()
        mock_offer.description = "PYTHON developer needed"
        
        mock_db.query.return_value.all.return_value = [mock_offer]
        
        result = analyze_technology_demand(mock_db)
        python_count = next((item['count'] for item in result if item['technology'] == 'Python'), 0)
        
        assert python_count == 1 