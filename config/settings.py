import os
from dotenv import load_dotenv
load_dotenv()

NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

OUTPUT_FILE = 'top5_news.json'
MAX_ARTICLES = 10
TOP_ARTICLES = 5