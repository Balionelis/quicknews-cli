import sys
import time
import itertools
from concurrent.futures import ThreadPoolExecutor

# Shows some animation thing
def loading_animation(duration=5):
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    end_time = time.time() + duration
    
    while time.time() < end_time:
        sys.stdout.write('\rLoading ' + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
    
    sys.stdout.write('\r          \r')
    sys.stdout.flush()

def run_with_spinner(func, *args, **kwargs):
    with ThreadPoolExecutor(max_workers=1) as executor:
        animation_future = executor.submit(loading_animation)
        result = func(*args, **kwargs)
        animation_future.result()
    return result