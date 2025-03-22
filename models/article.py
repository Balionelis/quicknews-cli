class Article:
    def __init__(self, title="No title", url="#"):
        self.title = title
        self.url = url
    
    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url
        }

def extract_article_data(articles, picked_numbers):
    top_news = []
    for i in picked_numbers:
        if i < len(articles):
            article = articles[i]
            top_news.append(Article(
                article.get("title", "No title"),
                article.get("url", "#")
            ))
    return top_news

def format_selected_titles(articles, picked_numbers):
    selected_titles = []
    for i, index in enumerate(picked_numbers):
        if index < len(articles):
            title = articles[index].get("title", "No title")
            selected_titles.append(f"{i+1}. {title}")
    
    return "\n".join(selected_titles)