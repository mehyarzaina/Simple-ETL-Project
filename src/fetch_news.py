import requests
from sqlmodel import select
from database import get_session
from models import Article, ArticleCategory
from helper import list_to_string, parse_pub_date
from config import API_KEY

API_URL = f"https://newsdata.io/api/1/latest?apikey={API_KEY}"

def fetch_and_store_news():
    print("Fetching news from API...")

    try:
        response = requests.get(API_URL, timeout=30) #call api
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return
    
    #extract API
    data = response.json()
    results = data.get("results", []) #list of articles

    if not results:
        print("No articles found.")
        return

    with get_session() as session:
        new_count = 0

        for item in results:
            article_id = item.get("article_id")
            if not article_id:
                continue

            # Skip duplicates
            existing = session.exec(
                select(Article).where(Article.article_id == article_id)
            ).first()
            if existing:
                continue

            # Create article object
            article = Article(
                article_id=article_id,
                link=item.get("link"),
                title=item.get("title"),
                creator=list_to_string(item.get("creator")),
                language=item.get("language"),
                country=list_to_string(item.get("country")),
                fetched_at=parse_pub_date(item.get("pubDate")),
            )

            # Add categories
            category_list = item.get("category", [])
            for cat_name in category_list:
                category_obj = ArticleCategory(category_name=cat_name)
                article.categories.append(category_obj)

            session.add(article) #Load ETL
            new_count += 1

        session.commit() #Load ETL

    print(f"{new_count} new articles stored successfully.")