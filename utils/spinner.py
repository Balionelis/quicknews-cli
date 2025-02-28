import sys
import time
import threading
import itertools
from concurrent.futures import ThreadPoolExecutor

class Spinner:
    def __init__(self, message="Loading"):
        self.message = message
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.running = False
        self.spinner_thread = None

    def start(self):
        self.running = True
        self.spinner_thread = threading.Thread(target=self._spin)
        self.spinner_thread.start()

    def stop(self):
        self.running = False
        if self.spinner_thread:
            self.spinner_thread.join()
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()

    def _spin(self):
        while self.running:
            sys.stdout.write('\r' + self.message + ' ' + next(self.spinner))
            sys.stdout.flush()
            time.sleep(0.1)

def run_with_spinner(message, func, *args, **kwargs):
    spinner = Spinner(message)
    result = None
    exception = None
    
    try:
        spinner.start()
        result = func(*args, **kwargs)
    except Exception as e:
        exception = e
    finally:
        spinner.stop()
    
    if exception:
        raise exception
    
    return result