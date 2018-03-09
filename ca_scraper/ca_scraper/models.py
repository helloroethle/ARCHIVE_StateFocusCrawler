from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import ca_scraper.settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**ca_scraper.settings.DATABASE))


def create_articles_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Articles(DeclarativeBase):
    """Sqlalchemy articles model"""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    source = Column('source', String)
    title = Column('title', String)
    url = Column('url', String, nullable=True)
    author = Column('author', String)
    content = Column('content', String)
    published = Column('published', DateTime, nullable=True)
    issues = Column('issues', String)
    blob_keywords = Column('blob_keywords', String)
    rake_keywords = Column('rake_keywords', String)
    blob_sentiment = Column('blob_sentiment', String)
    nltk_sentiment = Column('nltk_sentiment', String)