import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.ai_service import setup_gemini, get_ai_selection, parse_ai_selection

class TestAIService(unittest.TestCase):
    
    @patch('services.ai_service.genai')
    def test_setup_gemini_success(self, mock_genai):
        setup_gemini()
        mock_genai.configure.assert_called_once()
    
    @patch('services.ai_service.genai')
    def test_setup_gemini_failure(self, mock_genai):
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
