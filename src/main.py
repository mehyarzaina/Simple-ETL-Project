import schedule
import time
from fetch_news import fetch_and_store_news
from models import Article, ArticleCategory
from database import engine
from sqlmodel import SQLModel

def job():
    SQLModel.metadata.create_all(engine)
    fetch_and_store_news()

# Run once at start
job()

# Schedule every 2 hours
schedule.every(2).hours.do(job)

#schedule.every(2).minutes.do(job)

print("Scheduler started... Fetching news every 2 hours.")

while True:
    schedule.run_pending()
    time.sleep(60)  