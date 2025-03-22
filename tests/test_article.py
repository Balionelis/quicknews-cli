import unittest
from models.article import Article, extract_article_data

class TestArticle(unittest.TestCase):
    def test_article_initialization(self):
        article = Article("Test Title", "http://example.com")
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.url, "http://example.com")
    
    def test_article_default_values(self):
        article = Article()
        self.assertEqual(article.title, "No title")
        self.assertEqual(article.url, "#")
    
    def test_article_to_dict(self):
        article = Article("Test Title", "http://example.com")
        article_dict = article.to_dict()
        self.assertEqual(article_dict, {
            "title": "Test Title",
            "url": "http://example.com"
        })

    def test_extract_article_data(self):
        articles = [
            {"title": "Title 1", "url": "url1"},
            {"title": "Title 2", "url": "url2"},
            {"title": "Title 3", "url": "url3"},
        ]
        
        picked_numbers = [0, 2]
        result = extract_article_data(articles, picked_numbers)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Title 1")
        self.assertEqual(result[0].url, "url1")
        self.assertEqual(result[1].title, "Title 3")
        self.assertEqual(result[1].url, "url3")
    
    def test_extract_article_data_out_of_range(self):
        articles = [
            {"title": "Title 1", "url": "url1"},
            {"title": "Title 2", "url": "url2"},
        ]
        
        picked_numbers = [0, 2, 3]
        result = extract_article_data(articles, picked_numbers)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Title 1")
        self.assertEqual(result[0].url, "url1")

if __name__ == '__main__':
    unittest.main()