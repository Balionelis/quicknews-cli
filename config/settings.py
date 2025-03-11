import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

OUTPUT_FILE = 'top5_news.json'
MAX_ARTICLES = 20
TOP_ARTICLES = 5