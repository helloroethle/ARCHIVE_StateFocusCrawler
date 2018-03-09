# -*- coding: utf-8 -*-
from scrapy.item import Item, Field
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

class Article(Item):
    """Livingsocial container (dictionary-like object) for scraped data"""
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