import unittest
from unittest.mock import patch, MagicMock
import os
import io
import sys
from services.ai_service import setup_gemini, get_ai_selection, parse_ai_selection, cleanup_gemini

class TestAIService(unittest.TestCase):
    @patch('atexit.register')
    @patch('google.generativeai.configure')
    def test_setup_gemini(self, mock_configure, mock_atexit):
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            setup_gemini()
            mock_configure.assert_called_once()
            mock_atexit.assert_called_once()

    @patch('google.generativeai.GenerativeModel')
    def test_get_ai_selection(self, mock_gen_model):
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "1,2,3,4,5"
        mock_model.generate_content.return_value = mock_response
        mock_gen_model.return_value = mock_model
        
        result = get_ai_selection("test query", "1. Title 1\n2. Title 2")
        self.assertEqual(result, "1,2,3,4,5")
        mock_model.generate_content.assert_called_once()

    @patch('google.generativeai.GenerativeModel')
    def test_get_ai_selection_retry(self, mock_gen_model):
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = [Exception("API Error"), MagicMock(text="1,2,3")]
        mock_gen_model.return_value = mock_model
        
        result = get_ai_selection("test query", "1. Title 1\n2. Title 2", max_retries=2)
        self.assertEqual(result, "1,2,3")
        self.assertEqual(mock_model.generate_content.call_count, 2)

    @patch('google.generativeai.GenerativeModel')
    def test_get_ai_selection_all_retries_fail(self, mock_gen_model):
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_gen_model.return_value = mock_model
        
        result = get_ai_selection("test query", "1. Title 1\n2. Title 2", max_retries=2, retry_delay=0)
        self.assertEqual(result, "1,2,3,4,5")
        self.assertEqual(mock_model.generate_content.call_count, 2)

    def test_parse_ai_selection_valid(self):
        result = parse_ai_selection("1, 3, 5", 5, top_count=3)
        self.assertEqual(result, [0, 2, 4])

    def test_parse_ai_selection_out_of_range(self):
        result = parse_ai_selection("1, 10, 5", 5, top_count=3)
        self.assertEqual(result, [0, 4])

    def test_parse_ai_selection_invalid(self):
        result = parse_ai_selection("invalid, format", 5, top_count=3)
        self.assertEqual(result, [0, 1, 2])

    def test_parse_ai_selection_empty(self):
        result = parse_ai_selection("", 5, top_count=3)
        self.assertEqual(result, [0, 1, 2])

    @patch('gc.collect')
    def test_cleanup_gemini(self, mock_gc):
        cleanup_gemini()
        mock_gc.assert_called_once()

if __name__ == '__main__':
    unittest.main()