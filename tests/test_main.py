import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
import json

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
    
    @patch('builtins.open')
    def test_save_news_to_file_exception(self, mock_open):
        # Test error handling when saving fails
        mock_open.side_effect = IOError("File error")
        
        article = MagicMock()
        article.to_dict.return_value = {"title": "Title", "description": "Desc", "url": "url"}
        
        # Should not raise exception
        with patch('builtins.print') as mock_print:
            save_news_to_file([article], "test_file.json")
            mock_print.assert_any_call("Error saving news to file: File error")
    
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
    
    @patch('main.setup_gemini')
    @patch('main.input', return_value="test query")
    @patch('main.run_with_spinner')
    @patch('main.extract_titles')
    @patch('main.format_titles_for_ai')
    @patch('main.parse_ai_selection')
    @patch('main.extract_article_data')
    @patch('main.save_news_to_file')
    @patch('main.display_news')
    @patch('main.print')
    def test_main_success(self, mock_print, mock_display, mock_save, mock_extract_data,
                        mock_parse, mock_format, mock_extract_titles, mock_spinner, 
                        mock_input, mock_setup):
        # Configure mocks for the success path
        mock_spinner.side_effect = [
            None,  # setup_gemini result
            ["article1", "article2"],  # fetch_news result
            "AI answer",  # get_ai_selection result
            ["processed article1", "processed article2"]  # extract_article_data result
        ]
        
        mock_extract_titles.return_value = ["title1", "title2"]
        mock_format.return_value = "formatted titles"
        mock_parse.return_value = [0, 1]
        
        # Call main function
        main()
        
        # Verify the flow
        mock_input.assert_called_once()
        mock_spinner.assert_called()
        mock_extract_titles.assert_called_once()
        mock_format.assert_called_once()
        mock_parse.assert_called_once()
        mock_save.assert_called_once()
        mock_display.assert_called_once()
        mock_print.assert_any_call("✓ Complete!")
    
    @patch('main.setup_gemini')
    @patch('main.input', return_value="test query")
    @patch('main.run_with_spinner')
    @patch('main.sys.exit')
    def test_main_no_articles(self, mock_exit, mock_spinner, mock_input, mock_setup):
        # Configure mock to return empty list for fetch_news
        mock_spinner.side_effect = [
            None,  # setup_gemini result
            []  # fetch_news result (empty)
        ]
        
        # Make sys.exit raise an exception to catch it
        mock_exit.side_effect = SystemExit
        
        # Call main function - this should exit
        with self.assertRaises(SystemExit):
            main()
        
        # Verify correct exit
        mock_exit.assert_called_once_with(0)
    
    @patch('main.setup_gemini')
    @patch('main.input', return_value="test query")
    @patch('main.run_with_spinner')
    def test_main_exception(self, mock_spinner, mock_input, mock_setup):
        # Simulate an unexpected exception
        mock_spinner.side_effect = Exception("Test error")
        
        # Call main function
        with patch('main.sys.exit') as mock_exit:
            mock_exit.side_effect = SystemExit
            
            with self.assertRaises(SystemExit):
                main()
            
            # Should exit with code 1 (error)
            mock_exit.assert_called_once_with(1)
    
    @patch('main.setup_gemini')
    @patch('main.input')
    def test_main_keyboard_interrupt(self, mock_input, mock_setup):
        # Simulate user interruption
        mock_input.side_effect = KeyboardInterrupt
        
        # Call main function
        with patch('main.sys.exit') as mock_exit:
            mock_exit.side_effect = SystemExit
            
            with self.assertRaises(SystemExit):
                main()
            
            # Should exit with code 0 (normal)
            mock_exit.assert_called_once_with(0)