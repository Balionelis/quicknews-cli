import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import threading

# Add the parent directory to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.spinner import Spinner, run_with_spinner

class TestSpinner(unittest.TestCase):
    
    @patch('utils.spinner.sys.stdout')
    def test_spinner_start_stop(self, mock_stdout):
        # Test that the spinner starts and stops correctly
        spinner = Spinner("Testing")
        
        # Create a mock thread
        mock_thread = MagicMock()
        
        # Patch both the Thread class and its start method
        with patch('threading.Thread', return_value=mock_thread):
            spinner.start()
            self.assertTrue(spinner.running)
            self.assertIsNotNone(spinner.spinner_thread)
            mock_thread.start.assert_called_once()
            
            spinner.stop()
            self.assertFalse(spinner.running)
            mock_thread.join.assert_called_once()
            
            # Check that write was called to clear the line
            mock_stdout.write.assert_called()
            mock_stdout.flush.assert_called()
    
    @patch('utils.spinner.time.sleep')
    @patch('utils.spinner.sys.stdout')
    def test_spinner_spin_method(self, mock_stdout, mock_sleep):
        # Test the _spin method directly
        spinner = Spinner("Testing")
        spinner.running = True
        
        # Mock the running flag to stop after one iteration
        def stop_after_one_iteration(*args, **kwargs):
            spinner.running = False
            
        mock_sleep.side_effect = stop_after_one_iteration
        
        # Call the spin method
        spinner._spin()
        
        # Check that write and flush were called
        mock_stdout.write.assert_called_once()
        mock_stdout.flush.assert_called_once()
    
    def test_run_with_spinner_success(self):
        # Test successful function execution
        test_func = MagicMock(return_value="test result")
        
        with patch('utils.spinner.Spinner') as MockSpinner:
            mock_spinner_instance = MockSpinner.return_value
            
            result = run_with_spinner("Test message", test_func, "arg1", kwarg1="value")
            
            # Verify spinner was started and stopped
            mock_spinner_instance.start.assert_called_once()
            mock_spinner_instance.stop.assert_called_once()
            
            # Verify function was called with args
            test_func.assert_called_once_with("arg1", kwarg1="value")
            
            # Verify correct result returned
            self.assertEqual(result, "test result")
    
    def test_run_with_spinner_exception(self):
        # Test function that raises an exception
        test_func = MagicMock(side_effect=ValueError("Test error"))
        
        with patch('utils.spinner.Spinner') as MockSpinner:
            mock_spinner_instance = MockSpinner.return_value
            
            # Should re-raise the exception
            with self.assertRaises(ValueError):
                run_with_spinner("Test message", test_func)
            
            mock_spinner_instance.start.assert_called_once()
            mock_spinner_instance.stop.assert_called_once()