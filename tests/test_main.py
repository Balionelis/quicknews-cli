import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os

# Add the parent directory to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import save_news_to_file, display_news, main

class TestMain(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_news_to_file(self, mock_json_dump, mock_file_open):
        # Create mock articles
        article1 = MagicMock()
        article1.to_dict.return_value = {"title": "Title 1", "description": "Desc 1", "url": "url1"}
        
        article2 = MagicMock()
        article2.to_dict.return_value = {"title": "Title 2", "description": "Desc 2", "url": "url2"}
        
        top_news = [article1, article2]
        
        # Call function
        save_news_to_file(top_news, "test_file.json")
        
        # Verify file was opened correctly
        mock_file_open.assert_called_once_with("test_file.json", "w")
        
        # Verify json.dump was called with correct arguments
        expected_data = [
            {"title": "Title 1", "description": "Desc 1", "url": "url1"},
            {"title": "Title 2", "description": "Desc 2", "url": "url2"}
        ]
        mock_json_dump.assert_called_once()
        self.assertEqual(mock_json_dump.call_args[0][0], expected_data)
    
    @patch('builtins.print')
    def test_display_news(self, mock_print):
        # Create mock articles
        article1 = MagicMock()
        article1.title = "Title 1"
        article1.description = "Desc 1"
        article1.url = "url1"
        
        article2 = MagicMock()
        article2.title = "Title 2"
        article2.description = "Desc 2"
        article2.url = "url2"
        
        top_news = [article1, article2]
        
        # Call function
        display_news(top_news)
        
        # Verify print was called with correct arguments
        expected_calls = [
            unittest.mock.call("\nHere's your news:\n"),
            unittest.mock.call("1. Title 1"),
            unittest.mock.call("   Desc 1"),
            unittest.mock.call("   Link: url1"),
            unittest.mock.call(""),
            unittest.mock.call("2. Title 2"),
            unittest.mock.call("   Desc 2"),
            unittest.mock.call("   Link: url2"),
            unittest.mock.call("")
        ]
        mock_print.assert_has_calls(expected_calls)
    
    @patch('main.print')
    @patch('main.display_news')
    @patch('main.save_news_to_file')
    @patch('main.extract_article_data')
    @patch('main.parse_ai_selection')
    @patch('main.run_with_spinner')
    @patch('main.format_titles_for_ai')
    @patch('main.extract_titles')
    @patch('main.fetch_news')
    @patch('main.input', return_value="test query")
    @patch('main.setup_gemini')
    def test_main_success(self, mock_setup, mock_input, mock_fetch, mock_extract_titles, 
                        mock_format, mock_spinner, mock_parse, mock_extract_data, 
                        mock_save, mock_display, mock_print):
        # Configure mocks
        mock_fetch.return_value = ["article1", "article2"]
        mock_extract_titles.return_value = ["title1", "title2"]
        mock_format.return_value = "formatted titles"
        mock_spinner.return_value = "AI answer"
        mock_parse.return_value = [0, 1]
        mock_extract_data.return_value = ["processed article1", "processed article2"]
        
        # Call main function
        main()
        
        # Verify everything was called in correct order
        mock_input.assert_called_once()
        mock_fetch.assert_called_once_with("test query")
        mock_extract_titles.assert_called_once()
        mock_format.assert_called_once()
        mock_spinner.assert_called_once()
        mock_parse.assert_called_once()
        mock_extract_data.assert_called_once()
        mock_save.assert_called_once()
        mock_display.assert_called_once()
        mock_print.assert_any_call("✓ Complete!")
    
    @patch('main.setup_gemini')
    @patch('main.input', return_value="test query")
    @patch('main.fetch_news')
    @patch('main.sys.exit')
    def test_main_no_articles(self, mock_exit, mock_fetch, mock_input, mock_setup):
        # Configure mock to return empty list
        mock_fetch.return_value = []
        
        # Make sys.exit raise an exception to stop execution at first call
        mock_exit.side_effect = SystemExit
        
        # Call main function - this should exit at first sys.exit call
        with patch('main.get_ai_selection') as mock_get_ai:
            with self.assertRaises(SystemExit):
                main()
            
            # Verify get_ai_selection was not called
            mock_get_ai.assert_not_called()