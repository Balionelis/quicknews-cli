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
