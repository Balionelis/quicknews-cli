import sys
import requests
from datetime import date, timedelta
from config.settings import NEWSAPI_KEY, MAX_ARTICLES

# Gets the news
def fetch_news(query, timeout=10):
    yesterday = date.today() - timedelta(days=1)
    news_url = f"https://newsapi.org/v2/everything?q={query}&from={yesterday}&sortBy=relevancy&language=en&apiKey={NEWSAPI_KEY}"
    
    try:
        response = requests.get(news_url, timeout=timeout)
        
        if response.status_code == 429:
            print("Rate limit exceeded for NewsAPI. Please try again later.")
            sys.exit(1)
        
        if response.status_code != 200:
            print(f"Error getting news: {response.status_code}")
            if response.status_code == 401:
                print("API key may be invalid or expired.")
            sys.exit(1)
        
        news_data = response.json()
        return news_data.get("articles", [])
    
    except requests.exceptions.Timeout:
        print("Request to NewsAPI timed out. Please check your internet connection and try again.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your internet connection and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error fetching news: {str(e)}")
        sys.exit(1)

# Gets the titles
def extract_titles(articles):
    titles = []
    for i in range(min(MAX_ARTICLES, len(articles))):
        titles.append(articles[i].get("title", "No title"))
    
    return titles

# Makes a list for the AI
def format_titles_for_ai(titles):
    return "\n".join(f"{i+1}. {title}" for i, title in enumerate(titles))