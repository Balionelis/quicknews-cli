import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, timedelta
from config.settings import MAX_ARTICLES

def fetch_news(query, timeout=10):
    query = urllib.parse.quote_plus(query)
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://news.google.com/rss/search?q={query}+after:{today}&hl=en-US&gl=US&ceid=US:en"
    
    try:
        response = requests.get(url, timeout=timeout)
        
        if response.status_code != 200:
            print(f"Error getting news: {response.status_code}")
            sys.exit(1)
        
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        articles = []
        for item in items:
            title = item.title.text if item.title else "No title"
            link = item.link.text if item.link else "#"
            pub_date = item.pubDate.text if item.pubDate else ""
            
            parsed_url = urllib.parse.urlparse(link)
            clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            
            articles.append({
                "title": title,
                "url": clean_url,
                "publishedAt": pub_date
            })
        
        return articles
    
    except requests.exceptions.Timeout:
        print("Request to Google News timed out. Please check your internet connection and try again.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your internet connection and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error fetching news: {str(e)}")
        sys.exit(1)

def extract_titles(articles):
    titles = []
    for i in range(min(MAX_ARTICLES, len(articles))):
        titles.append(articles[i].get("title", "No title"))
    
    return titles

def format_titles_for_ai(titles):
    return "\n".join(f"{i+1}. {title}" for i, title in enumerate(titles))