import sys
import time
import os
import threading
import atexit
import contextlib
import io

os.environ['GRPC_WAIT_FOR_READY'] = 'false'
os.environ['GRPC_DNS_RESOLVER'] = 'native'

import google.generativeai as genai
from config.settings import GEMINI_API_KEY

exit_handler_registered = False

def force_exit():
    os._exit(0)

def setup_gemini():
    global exit_handler_registered
    
    try:
        if not exit_handler_registered:
            atexit.register(force_exit)
            exit_handler_registered = True
            
            import signal
            def handle_exit(signum, frame):
                sys.exit(0)
                
            signal.signal(signal.SIGINT, handle_exit)
            signal.signal(signal.SIGTERM, handle_exit)
        
        with contextlib.redirect_stderr(io.StringIO()):
            genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error with Gemini API setup: {e}")
        print("Please check your API key and internet connection.")
        sys.exit(1)

def get_ai_selection(query, titles_text, max_retries=3, retry_delay=2):
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            model = genai.GenerativeModel("gemini-2.0-flash")
        
        ai_prompt = ( 
            f"I have a list of news headlines related to '{query}'.\n\n"
            f"Here are the headlines:\n{titles_text}\n\n"
            f"Your task is to select the 5 most important and relevant headlines based on their significance, impact, and relevance to '{query}'.\n"
            f"Only respond with the numbers of the selected headlines in a comma-separated format (e.g., 1,2,5,7,9) and nothing else."
        )
        retries = 0
        while retries < max_retries:
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    response = model.generate_content(ai_prompt)
                return response.text.strip()
            except Exception as e:
                retries += 1
                if retries >= max_retries:
                    print(f"Failed to get AI selection after {max_retries} attempts: {str(e)}")
                    print("Using default selection instead.")
                    return "1,2,3,4,5"
                print(f"AI request failed, retrying ({retries}/{max_retries})...")
                time.sleep(retry_delay)
        
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        print("Using default selection instead.")
        return "1,2,3,4,5"

def get_ai_satisfaction(query, selected_titles, max_retries=3, retry_delay=2):
    default_satisfaction = 85
    
    ai_prompt = (
        f"You selected the following headlines for the query '{query}':\n\n"
        f"{selected_titles}\n\n"
        f"On a scale from 0% to 100%, how satisfied are you with these selections in terms of relevance and importance?\n"
        f"Please respond with just a percentage number (e.g., 85) and nothing else."
    )
    
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            model = genai.GenerativeModel("gemini-2.0-flash")
            
        for retry in range(max_retries):
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    response = model.generate_content(ai_prompt)
                result = response.text.strip()
                result = ''.join(c for c in result if c.isdigit())
                if result and 0 <= int(result) <= 100:
                    return int(result)
                return default_satisfaction
            except Exception:
                if retry >= max_retries - 1:
                    break
                print(f"AI satisfaction request failed, retrying ({retry+1}/{max_retries})...")
                time.sleep(retry_delay)
    except Exception as e:
        print(f"Error with Gemini API during satisfaction check: {e}")
        
    return default_satisfaction

def parse_ai_selection(ai_answer, titles_length, top_count=5):
    try:
        picked_numbers = []
        for item in ai_answer.split(','):
            item = item.strip()
            if item.isdigit():
                num = int(item)
                if 1 <= num <= titles_length:
                    picked_numbers.append(num - 1)
        
        if len(picked_numbers) == 0 or len(picked_numbers) > top_count:
            picked_numbers = list(range(min(top_count, titles_length)))
        
        return picked_numbers[:top_count]
    except Exception as e:
        print(f"Error parsing AI selection: {str(e)}")
        return list(range(min(top_count, titles_length)))

def cleanup_gemini():
    try:
        import requests
        requests.Session().close()
    except:
        pass
    
    import gc
    gc.collect()