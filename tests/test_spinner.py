import unittest
from unittest.mock import patch, MagicMock
import sys
import time
import threading
from io import StringIO
from utils.spinner import Spinner, run_with_spinner

class TestSpinner(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_spinner_start_stop(self, mock_stdout):
        spinner = Spinner("Testing")
        spinner.start()
        time.sleep(0.2)  # Allow spinner to make at least one iteration
        spinner.stop()
        output = mock_stdout.getvalue()
        self.assertIn("Testing", output)
        self.assertTrue(any(c in output for c in ['-', '/', '|', '\\']))

    @patch('threading.Thread')
    def test_spinner_thread_creation(self, mock_thread):
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance
        
        spinner = Spinner("Testing")
        spinner.start()
        
        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()
        
        spinner.stop()
        mock_thread_instance.join.assert_called_once()

    def test_run_with_spinner_success(self):
        def sample_func(a, b):
            return a + b
        
        result = run_with_spinner("Adding", sample_func, 2, 3)
        self.assertEqual(result, 5)

    def test_run_with_spinner_exception(self):
        def failing_func():
            raise ValueError("Test exception")
        
        with self.assertRaises(ValueError):
            run_with_spinner("Testing", failing_func)

if __name__ == '__main__':
    unittest.main()