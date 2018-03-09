# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from ca_scraper.models import Articles, db_connect, create_articles_table
from ca_scraper.items import Article
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
class ArticleSavePipeline(object):
   def __init__(self):
      engine = db_connect()
      create_articles_table(engine)
      self.Session = sessionmaker(bind=engine)
   def process_item(self, item, spider):
      if isinstance(item, Article):
         return self.handleArticle(item, spider)
   def handleArticle(self, item, spider):
      print('****** article end *******')
      session = self.Session()
      article = Articles(**item)
      try:
         session.add(article)
         session.commit()
      except:
         session.rollback()
         raise
      finally:
         session.close()
      return item