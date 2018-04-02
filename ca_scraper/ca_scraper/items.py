# -*- coding: utf-8 -*-
from scrapy.item import Item, Field
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

class Article(Item):
    title = Field()
    source = Field()
    url = Field()
    author = Field()
    content = Field()
    published = Field()
    issues = Field()
    blob_keywords = Field()
    rake_keywords = Field()
    blob_sentiment = Field()
    nltk_sentiment = Field()
    readability = Field()
    word_frequency = Field()
    word_count = Field()
    unique_word_count = Field()

class PressRelease(Item):
    title = Field()
    url = Field()
    legislator = Field()
    content = Field()
    published = Field()
    issues = Field()
    blob_keywords = Field()
    rake_keywords = Field()
    blob_sentiment = Field()
    nltk_sentiment = Field()
    readability = Field()
    word_frequency = Field()
    word_count = Field()
    unique_word_count = Field()

class Legislator(Item):
    state = Field()
    house = Field()
    district = Field()
    party = Field()
    name = Field()
    official_site_url = Field()
    img_src = Field()
    readability = Field()
    press_release_count = Field()
    article_count = Field()
    issue_overview = Field()
    source_overview = Field()
    sentiment_overview = Field()
    word_frequency = Field()
    keywords = Field()
