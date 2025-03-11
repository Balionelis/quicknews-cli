import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import json
import sys
from main import save_news_to_file, display_news, main
from models.article import Article

class TestMain(unittest.TestCase):
    @patch('builtins.open')
    def test_save_news_to_file(self, mock_file):
        mock_file_handle = mock_open()
        mock_file.return_value = mock_file_handle()
        
        articles = [
            Article("Title 1", "url1"),
            Article("Title 2", "url2")
        ]
        
        save_news_to_file(articles, "test.json")
        
        mock_file.assert_called_once_with("test.json", 'w')
        
        expected_data = [
            {"title": "Title 1", "url": "url1"},
            {"title": "Title 2", "url": "url2"}
        ]
        
        mock_file_handle().write.assert_called()

    @patch('builtins.open')
    def test_save_news_to_file_exception(self, mock_open):
        mock_open.side_effect = Exception("File error")
        articles = [Article("Title 1", "url1")]
        
        save_news_to_file(articles, "test.json")

    @patch('builtins.print')
    def test_display_news(self, mock_print):
        articles = [
            Article("Title 1", "url1"),
            Article("Title 2", "url2")
        ]
        
        display_news(articles)
        
        self.assertTrue(mock_print.call_count > 5)
        
        print_calls = [call_args[0][0] for call_args in mock_print.call_args_list]
        self.assertTrue(any("[1] Title 1" in str(call_arg) for call_arg in print_calls))
        self.assertTrue(any("[2] Title 2" in str(call_arg) for call_arg in print_calls))
        self.assertTrue(any("🔗 url1" in str(call_arg) for call_arg in print_calls))
        self.assertTrue(any("🔗 url2" in str(call_arg) for call_arg in print_calls))

    @patch('main.run_with_spinner')
    @patch('main.input', return_value="test query")
    @patch('main.save_news_to_file')
    @patch('main.display_news')
    @patch('services.news_service.extract_titles')
    @patch('services.news_service.format_titles_for_ai')
    @patch('services.ai_service.get_ai_selection')
    @patch('services.ai_service.parse_ai_selection')
    @patch('models.article.extract_article_data')
    def test_main_success(self, mock_extract_article, mock_parse_ai, 
                          mock_get_ai, mock_format_titles, mock_extract_titles,
                          mock_display, mock_save, mock_input, mock_spinner):
        mock_articles = [{"title": "Title 1", "url": "url1"}]
        mock_titles = ["Title 1"]
        mock_titles_text = "1. Title 1"
        mock_ai_answer = "1"
        mock_picked_numbers = [0]
        mock_top_news = [Article("Title 1", "url1")]
        
        mock_extract_titles.return_value = mock_titles
        mock_format_titles.return_value = mock_titles_text
        mock_get_ai.return_value = mock_ai_answer
        mock_parse_ai.return_value = mock_picked_numbers
        mock_extract_article.return_value = mock_top_news
        
        def spinner_side_effect(message, func, *args, **kwargs):
            if func.__name__ == "setup_gemini":
                return None
            elif func.__name__ == "fetch_news":
                return mock_articles
            elif func.__name__ == "get_ai_selection":
                return mock_ai_answer
            elif func.__name__ == "extract_article_data":
                return mock_top_news
        
        mock_spinner.side_effect = spinner_side_effect
        
        main()
        
        mock_save.assert_called_once()
        mock_display.assert_called_once_with(mock_top_news)

    @patch('main.run_with_spinner')
    @patch('main.input', return_value="test query")
    def test_main_no_articles(self, mock_input, mock_spinner):
        def spinner_side_effect(message, func, *args, **kwargs):
            if "Fetching news" in message:
                return []
            return None
        
        mock_spinner.side_effect = spinner_side_effect
        
        with self.assertRaises(SystemExit):
            main()

if __name__ == '__main__':
    unittest.main()