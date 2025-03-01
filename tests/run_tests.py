import unittest
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="google._upb._message")

def run_all_tests():
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir)
    
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    run_all_tests()