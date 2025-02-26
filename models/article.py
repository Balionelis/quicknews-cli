class Article:
    def __init__(self, title="No title", description="No description", url="#"):
        self.title = title
        self.description = description
        self.url = url
    
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "url": self.url
        }

def extract_article_data(articles, picked_numbers):
    top_news = []
    for i in picked_numbers:
        if i < len(articles):
            article = articles[i]
            top_news.append(Article(
                article.get("title", "No title"),
                article.get("description", "No description"),
                article.get("url", "#")
            ))
    return top_news
