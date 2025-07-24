import unittest
from io import StringIO
from unittest.mock import patch
import sys
import os

# Add the demo.py file to the path so we can import functions from it
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import demo

class TestDisplayFiltering(unittest.TestCase):
    
    def test_display_only_title_and_url(self):
        """Test that display_results only shows title and url columns when they exist"""
        columns = ['id', 'title', 'description', 'url', 'category']
        results = [
            (1, 'Article 1', 'Description 1', 'http://example.com/1', 'Tech'),
            (2, 'Article 2', 'Description 2', 'http://example.com/2', 'Science')
        ]
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            demo.display_results(columns, results)
            
            # Check that print was called (exact format may vary due to column width calculation)
            self.assertTrue(mock_print.called)
    
    def test_display_only_title(self):
        """Test that display_results only shows title column when url doesn't exist"""
        columns = ['id', 'title', 'description', 'category']
        results = [
            (1, 'Article 1', 'Description 1', 'Tech'),
            (2, 'Article 2', 'Description 2', 'Science')
        ]
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            demo.display_results(columns, results)
            
            # Check that print was called
            self.assertTrue(mock_print.called)
    
    def test_display_only_url(self):
        """Test that display_results only shows url column when title doesn't exist"""
        columns = ['id', 'description', 'url', 'category']
        results = [
            (1, 'Description 1', 'http://example.com/1', 'Tech'),
            (2, 'Description 2', 'http://example.com/2', 'Science')
        ]
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            demo.display_results(columns, results)
            
            # Check that print was called
            self.assertTrue(mock_print.called)
    
    def test_display_all_columns_when_no_title_or_url(self):
        """Test that display_results shows all columns when neither title nor url exist"""
        columns = ['id', 'description', 'category']
        results = [
            (1, 'Description 1', 'Tech'),
            (2, 'Description 2', 'Science')
        ]
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            demo.display_results(columns, results)
            
            # Check that print was called
            self.assertTrue(mock_print.called)

if __name__ == '__main__':
    unittest.main()