import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import time

# Add the parent directory to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.spinner import loading_animation, run_with_spinner

class TestSpinner(unittest.TestCase):
    
    @patch('utils.spinner.time.sleep')
    @patch('utils.spinner.sys.stdout')
    def test_loading_animation(self, mock_stdout, mock_sleep):
        # Make time.time() first return a value and then return a value 
        # that's greater than the duration to end the loop
        with patch('utils.spinner.time.time', side_effect=[10, 10, 16]):
            loading_animation(5)
            # Check that write was called for the spinner and flush was called
            mock_stdout.write.assert_called()
            mock_stdout.flush.assert_called()
    
    @patch('utils.spinner.ThreadPoolExecutor')
    def test_run_with_spinner(self, mock_executor):
        # Setup mocks
        mock_future = MagicMock()
        mock_executor_instance = MagicMock()
        mock_executor_instance.__enter__.return_value.submit.return_value = mock_future
        mock_executor.return_value = mock_executor_instance
        
        # Test function
        test_func = MagicMock(return_value="test result")
        
        result = run_with_spinner(test_func, "arg1", kwarg1="value")
        
        # Verify spinner was started
        mock_executor_instance.__enter__.return_value.submit.assert_called_once()
        
        # Verify function was called with args
        test_func.assert_called_once_with("arg1", kwarg1="value")
        
        # Verify we waited for animation to complete
        mock_future.result.assert_called_once()
        
        # Verify correct result returned
        self.assertEqual(result, "test result")
