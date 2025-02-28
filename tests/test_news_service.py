import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import requests

# Add the parent directory to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.news_service import fetch_news, extract_titles, format_titles_for_ai

class TestNewsService(unittest.TestCase):
    
    @patch('os.environ.get')
    @patch('services.news_service.requests.get')
    def test_fetch_news_success(self, mock_get, mock_env_get):
        mock_env_get.return_value = 'fake-api-key'
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'articles': [
                {'title': 'Test Article 1', 'description': 'Test Description 1', 'url': 'http://test1.com'},
                {'title': 'Test Article 2', 'description': 'Test Description 2', 'url': 'http://test2.com'}
            ]
        }
        mock_get.return_value = mock_response
        
        result = fetch_news('test query')
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], 'Test Article 1')
        self.assertEqual(result[1]['url'], 'http://test2.com')
        mock_get.assert_called_once()
    
    @patch('services.news_service.requests.get')
    def test_fetch_news_failure(self, mock_get):
        # Mock failed response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        with self.assertRaises(SystemExit):
            fetch_news('test query')
    
    @patch('services.news_service.requests.get')
    def test_fetch_news_rate_limit(self, mock_get):
        # Mock rate limit response
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response
        
        with self.assertRaises(SystemExit):
            fetch_news('test query')
    
    @patch('services.news_service.requests.get')
    def test_fetch_news_timeout(self, mock_get):
        # Mock timeout
        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")
        
        with self.assertRaises(SystemExit):
            fetch_news('test query')
    
    @patch('services.news_service.requests.get')
    def test_fetch_news_connection_error(self, mock_get):
        # Mock connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        with self.assertRaises(SystemExit):
            fetch_news('test query')
    
    def test_extract_titles(self):
        articles = [
            {'title': 'Article 1', 'description': 'Description 1'},
            {'title': 'Article 2', 'description': 'Description 2'},
            {'title': 'Article 3', 'description': 'Description 3'},
        ]
        
        # Test with default MAX_ARTICLES
        with patch('services.news_service.MAX_ARTICLES', 2):
            titles = extract_titles(articles)
            self.assertEqual(len(titles), 2)
            self.assertEqual(titles[0], 'Article 1')
            self.assertEqual(titles[1], 'Article 2')
        
        # Test with fewer articles than MAX_ARTICLES
        with patch('services.news_service.MAX_ARTICLES', 5):
            titles = extract_titles(articles)
            self.assertEqual(len(titles), 3)
    
    def test_format_titles_for_ai(self):
        titles = ['Title 1', 'Title 2', 'Title 3']
        formatted = format_titles_for_ai(titles)
        
        expected = "1. Title 1\n2. Title 2\n3. Title 3"
        self.assertEqual(formatted, expected)