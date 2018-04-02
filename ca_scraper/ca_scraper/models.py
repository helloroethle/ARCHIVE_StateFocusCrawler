from sqlalchemy import create_engine, Column, Integer, String, DateTime, Integer, Numeric
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


class Legislators(DeclarativeBase):
    """Sqlalchemy articles model"""
    __tablename__ = "legislators"

    id = Column(Integer, primary_key=True)
    state = Column('state', String)
    house = Column('house', String)
    district = Column('district', String)
    party = Column('party', String)
    name = Column('name', String)
    official_site_url = Column('official_site_url', String)
    img_src = Column('img_src', String)
    readability = Column('readability', Numeric)
    press_release_count = Column('press_release_count', Integer)
    article_count = Column('article_count', Integer)
    issue_overview = Column('issue_overview', String)
    source_overview = Column('source_overview', String)
    sentiment_overview = Column('sentiment_overview', String)
    word_frequency = Column('word_frequency', String)
    keywords = Column('keywords', String)


class PressReleases(DeclarativeBase):
    """Sqlalchemy articles model"""
    __tablename__ = "press_releases"

    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    url = Column('url', String, nullable=True)
    legislator = Column('legislator', String)
    content = Column('content', String)
    published = Column('published', DateTime, nullable=True)
    issues = Column('issues', String)
    blob_keywords = Column('blob_keywords', String)
    rake_keywords = Column('rake_keywords', String)
    blob_sentiment = Column('blob_sentiment', String)
    nltk_sentiment = Column('nltk_sentiment', String)
    readability = Column('readability', String)
    word_frequency = Column('word_frequency', String)
    word_count = Column('word_count', Integer)
    unique_word_count = Column('unique_word_count', Integer)



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
    readability = Column('readability', String)
    word_frequency = Column('word_frequency', String)
    word_count = Column('word_count', Integer)
    unique_word_count = Column('unique_word_count', Integer)
