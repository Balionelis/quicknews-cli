import sys
import google.generativeai as genai
from config.settings import GEMINI_API_KEY

# Sets up the AI thingy
def setup_gemini():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error with Gemini: {e}")
        sys.exit(1)

# Uses the AI model to pick stuff
def get_ai_selection(query, titles_text):
    model = genai.GenerativeModel("gemini-2.0-flash")
    ai_prompt = f"Here are news about '{query}':\n{titles_text}\n\nPick 5 best ones. Just give me numbers like 1,2,3,4,5"
    response = model.generate_content(ai_prompt)
    return response.text.strip()

# Tries to figure out what the AI said
def parse_ai_selection(ai_answer, titles_length, top_count=5):
    picked_numbers = []
    for item in ai_answer.split(','):
        item = item.strip()
        if item.isdigit():
            num = int(item)
            if 1 <= num <= titles_length:
                picked_numbers.append(num - 1)  # convert to 0-index
    
    if len(picked_numbers) == 0 or len(picked_numbers) > top_count:
        picked_numbers = list(range(min(top_count, titles_length)))
    
    return picked_numbers[:top_count]