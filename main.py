import json
import sys
from config.settings import TOP_ARTICLES, OUTPUT_FILE
from utils.spinner import run_with_spinner
from services.news_service import fetch_news, extract_titles, format_titles_for_ai
from services.ai_service import setup_gemini, get_ai_selection, parse_ai_selection, get_ai_satisfaction
from models.article import extract_article_data, format_selected_titles

def save_news_to_file(top_news, filename=OUTPUT_FILE, satisfaction=None):
    try:
        news_data = [article.to_dict() for article in top_news]
        data_to_save = {
            "articles": news_data
        }
        
        if satisfaction is not None:
            data_to_save["ai_satisfaction"] = satisfaction
            
        with open(filename, 'w') as f:
            json.dump(data_to_save, f, indent=4)
    except Exception as e:
        print(f"Error saving news to file: {str(e)}")

def display_news(top_news, satisfaction=None):
    print("\n┌───────────────────────────────────────────────")
    print("│ 📰 TOP 5 NEWS RESULTS")
    print("└───────────────────────────────────────────────\n")
    
    for i, item in enumerate(top_news):
        print(f"[{i+1}] {item.title}")
        print(f"    🔗 {item.url}")
        print("")
    
    if satisfaction is not None:
        print(f"AI SATISFACTION RATING: {satisfaction}%")

def main():
    try:
        run_with_spinner("Setting up AI service", setup_gemini)
        
        query = input('What do you want to hear about? ')
        
        # Fetch news
        articles = run_with_spinner(f"Fetching news about {query}", fetch_news, query)
        
        if not articles:
            print(f"No news found about '{query}'")
            sys.exit(0)
        
        print(f"Found {len(articles)} articles about '{query}'")
        
        titles = extract_titles(articles)
        if not titles:
            print(f"No titles found for '{query}'")
            sys.exit(0)
        
        titles_text = format_titles_for_ai(titles)
        
        print("Asking AI to select the best articles...")
        ai_answer = run_with_spinner("Waiting for AI response", get_ai_selection, query, titles_text)
        
        picked_numbers = parse_ai_selection(ai_answer, len(titles), TOP_ARTICLES)
        
        top_news = run_with_spinner("Processing articles", extract_article_data, articles, picked_numbers)
        
        if not top_news:
            print("No articles could be processed. Please try again.")
            sys.exit(0)
        
        selected_titles = format_selected_titles(articles, picked_numbers)
        print("Asking AI about its satisfaction with the selections...")
        satisfaction = run_with_spinner("Getting AI satisfaction rating", get_ai_satisfaction, query, selected_titles)
    
        save_news_to_file(top_news, satisfaction=satisfaction)
        display_news(top_news, satisfaction=satisfaction)
        print(f"✓ {len(top_news)} news articles saved to {OUTPUT_FILE}")
        print("✓ Complete!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        print("Please try again later.")
        sys.exit(1)

if __name__ == "__main__":
    main()