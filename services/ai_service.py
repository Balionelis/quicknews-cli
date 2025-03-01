import sys
import time
import google.generativeai as genai
from config.settings import GEMINI_API_KEY

# Sets up the AI
def setup_gemini():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error with Gemini API setup: {e}")
        print("Please check your API key and internet connection.")
        sys.exit(1)

# Promts AI
def get_ai_selection(query, titles_text, max_retries=3, retry_delay=2):
    try:
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

# Tries to figure out what the AI said
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