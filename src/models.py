from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

class ArticleCategory(SQLModel, table=True):
    __tablename__ = "article_categories"  # Table name in DB
    id: Optional[int] = Field(default=None, primary_key=True)
    category_name: str = Field(index=True)

    # Must match the DB table name exactly
    article_id: Optional[int] = Field(default=None, foreign_key="articles.id")
    article: Optional["Article"] = Relationship(back_populates="categories")


class Article(SQLModel, table=True):
    __tablename__ = "articles"  
    id: Optional[int] = Field(default=None, primary_key=True)
    article_id: str = Field(index=True, unique=True, max_length=255)
    link: str = Field(max_length=2048)
    title: str = Field(max_length=1024)
    creator: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    fetched_at: Optional[datetime] = None

    categories: List[ArticleCategory] = Relationship(back_populates="article")


