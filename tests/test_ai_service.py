import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.ai_service import setup_gemini, get_ai_selection, parse_ai_selection

class TestAIService(unittest.TestCase):
    
    @patch('os.environ.get')
    @patch('services.ai_service.genai')
    def test_setup_gemini_success(self, mock_genai, mock_env_get):
        mock_env_get.return_value = 'fake-api-key'
        
        setup_gemini()
        mock_genai.configure.assert_called_once()

    @patch('os.environ.get')
    @patch('services.ai_service.genai')
    def test_setup_gemini_failure(self, mock_genai, mock_env_get):
        mock_env_get.return_value = 'fake-api-key'
        mock_genai.configure.side_effect = Exception("API Error")
        
        with self.assertRaises(SystemExit):
            setup_gemini()
    
    @patch('services.ai_service.genai.GenerativeModel')
    def test_get_ai_selection(self, mock_model_class):
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "1, 3, 5"
        
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        result = get_ai_selection("test query", "1. Title 1\n2. Title 2\n3. Title 3")
        
        self.assertEqual(result, "1, 3, 5")
        mock_model.generate_content.assert_called_once()
    
    @patch('services.ai_service.genai.GenerativeModel')
    @patch('services.ai_service.time.sleep')
    def test_get_ai_selection_with_retry(self, mock_sleep, mock_model_class):
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = [Exception("API Error"), MagicMock(text="1, 3, 5")]
        mock_model_class.return_value = mock_model
        
        result = get_ai_selection("test query", "1. Title 1\n2. Title 2\n3. Title 3", max_retries=2)
        
        self.assertEqual(result, "1, 3, 5")
        self.assertEqual(mock_model.generate_content.call_count, 2)
        mock_sleep.assert_called_once()
    
    @patch('services.ai_service.genai.GenerativeModel')
    @patch('services.ai_service.time.sleep')
    def test_get_ai_selection_max_retries_exceeded(self, mock_sleep, mock_model_class):
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_model_class.return_value = mock_model
        
        result = get_ai_selection("test query", "1. Title 1\n2. Title 2\n3. Title 3", max_retries=2)
        
        self.assertEqual(result, "1,2,3,4,5")
        self.assertEqual(mock_model.generate_content.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 1)
    
    def test_parse_ai_selection_valid(self):
        ai_answer = "1, 3, 5"
        result = parse_ai_selection(ai_answer, 5)
        
        self.assertEqual(result, [0, 2, 4])
    
    def test_parse_ai_selection_invalid(self):
        # Test with non-numeric response
        result = parse_ai_selection("one, two, three", 5)
        self.assertEqual(result, [0, 1, 2, 3, 4])
        
        # Test with out-of-range numbers
        result = parse_ai_selection("1, 6, 7", 5)
        self.assertEqual(result, [0])
        
        # Test with too many selections
        result = parse_ai_selection("1, 2, 3, 4, 5, 6", 5)
        self.assertEqual(result, [0, 1, 2, 3, 4])
        
    def test_parse_ai_selection_exception(self):
        # Create a mock that raises an exception when split is called
        mock_answer = MagicMock()
        mock_answer.split.side_effect = Exception("Test exception")
        
        # Test with input that causes exception
        with patch('builtins.print') as mock_print:
            result = parse_ai_selection(mock_answer, 5)
            self.assertEqual(result, [0, 1, 2, 3, 4])
            mock_print.assert_any_call("Error parsing AI selection: Test exception")