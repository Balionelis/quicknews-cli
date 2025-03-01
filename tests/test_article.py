import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.article import Article, extract_article_data

class TestArticle(unittest.TestCase):
    
    def test_article_initialization(self):
        # Test default values
        article = Article()
        self.assertEqual(article.title, "No title")
        self.assertEqual(article.description, "No description")
        self.assertEqual(article.url, "#")
        
        # Test custom values
        article = Article("Test Title", "Test Description", "http://test.com")
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.description, "Test Description")
        self.assertEqual(article.url, "http://test.com")
    
    def test_to_dict(self):
        article = Article("Test Title", "Test Description", "http://test.com")
        result = article.to_dict()
        
        expected = {
            "title": "Test Title",
            "description": "Test Description",
            "url": "http://test.com"
        }
        
        self.assertEqual(result, expected)
    
    def test_extract_article_data(self):
        articles = [
            {"title": "Title 1", "description": "Description 1", "url": "http://test1.com"},
            {"title": "Title 2", "description": "Description 2", "url": "http://test2.com"},
            {"title": "Title 3", "description": "Description 3", "url": "http://test3.com"}
        ]
        
        picked_numbers = [0, 2]
        
        result = extract_article_data(articles, picked_numbers)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Title 1")
        self.assertEqual(result[1].title, "Title 3")