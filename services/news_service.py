import sys
import requests
from datetime import date, timedelta
from config.settings import NEWSAPI_KEY, MAX_ARTICLES

# Gets the actual news stuff
def fetch_news(query):
    yesterday = date.today() - timedelta(days=1)
    news_url = f"https://newsapi.org/v2/everything?q={query}&from={yesterday}&sortBy=relevancy&language=en&apiKey={NEWSAPI_KEY}"
    print(f"Getting news about {query}...")
    
    response = requests.get(news_url)
    if response.status_code != 200:
        print(f"Error getting news: {response.status_code}")
        sys.exit(1)
    
    news_data = response.json()
    return news_data.get("articles", [])

# Gets the titles I guess
def extract_titles(articles):
    titles = []
    for i in range(min(MAX_ARTICLES, len(articles))):
        titles.append(articles[i].get("title", "No title"))
    
    return titles

# Makes a list for the AI or whatever
def format_titles_for_ai(titles):
    return "\n".join(f"{i+1}. {title}" for i, title in enumerate(titles))
