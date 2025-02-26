import json
import sys
from config.settings import TOP_ARTICLES, OUTPUT_FILE
from utils.spinner import run_with_spinner
from services.news_service import fetch_news, extract_titles, format_titles_for_ai
from services.ai_service import setup_gemini, get_ai_selection, parse_ai_selection
from models.article import extract_article_data

# Dumps it to a file
def save_news_to_file(top_news, filename=OUTPUT_FILE):
    news_data = [article.to_dict() for article in top_news]
    with open(filename, 'w') as f:
        json.dump(news_data, f, indent=4)
    print(f"Saved to {filename}")

# Prints the news to screen
def display_news(top_news):
    print("\nHere's your news:\n")
    for i, item in enumerate(top_news):
        print(f"{i+1}. {item.title}")
        print(f"   {item.description}")
        print(f"   Link: {item.url}")
        print("")

# Does all the stuff
def main():
    setup_gemini()
    query = input('What do you want to hear about? ')
    
    articles = fetch_news(query)
    if not articles:
        print(f"No news about {query}")
        sys.exit(0)
    
    titles = extract_titles(articles)
    titles_text = format_titles_for_ai(titles)
    
    ai_answer = run_with_spinner(get_ai_selection, query, titles_text)
    
    picked_numbers = parse_ai_selection(ai_answer, len(titles), TOP_ARTICLES)
    top_news = extract_article_data(articles, picked_numbers)
    
    save_news_to_file(top_news)
    display_news(top_news)
    print("Done!")

if __name__ == "__main__":
    main()