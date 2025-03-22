import unittest
from unittest.mock import patch, MagicMock
import requests
from services.news_service import fetch_news, extract_titles, format_titles_for_ai

class TestNewsService(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_news_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = """
        <rss>
            <channel>
                <item>
                    <title>Test Title 1</title>
                    <link>http://example.com/1</link>
                    <pubDate>Mon, 20 Jan 2020 12:00:00 GMT</pubDate>
                </item>
                <item>
                    <title>Test Title 2</title>
                    <link>http://example.com/2?param=test</link>
                    <pubDate>Mon, 20 Jan 2020 13:00:00 GMT</pubDate>
                </item>
            </channel>
        </rss>
        """
        mock_get.return_value = mock_response
        
        articles = fetch_news("test query")
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0]["title"], "Test Title 1")
        self.assertEqual(articles[0]["url"], "http://example.com/1")
        self.assertEqual(articles[1]["url"], "http://example.com/2")

    @patch('requests.get')
    def test_fetch_news_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with self.assertRaises(SystemExit):
            fetch_news("test query")

    @patch('requests.get')
    def test_fetch_news_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()
        
        with self.assertRaises(SystemExit):
            fetch_news("test query")

    @patch('requests.get')
    def test_fetch_news_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        with self.assertRaises(SystemExit):
            fetch_news("test query")

    def test_extract_titles(self):
        articles = [
            {"title": "Title 1"},
            {"title": "Title 2"},
            {"title": "Title 3"}
        ]
        
        with patch('services.news_service.MAX_ARTICLES', 2):
            titles = extract_titles(articles)
            self.assertEqual(len(titles), 2)
            self.assertEqual(titles, ["Title 1", "Title 2"])

    def test_format_titles_for_ai(self):
        titles = ["Title 1", "Title 2", "Title 3"]
        formatted = format_titles_for_ai(titles)
        expected = "1. Title 1\n2. Title 2\n3. Title 3"
        self.assertEqual(formatted, expected)

if __name__ == '__main__':
    unittest.main()