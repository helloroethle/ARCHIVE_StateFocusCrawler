import scrapy
from scrapy import signals
from sqlalchemy.orm import sessionmaker
from ca_scraper.models import Legislators, db_connect, create_articles_table
from datetime import datetime
from sqlalchemy import and_
import time
from ca_scraper.items import PressRelease

class StateSenateDemocratPressReleasesSpider(scrapy.Spider):
    name = 'state_senate_democrat_press_releases'
    def __init__(self):
      engine = db_connect()
      create_articles_table(engine)
      self.Session = sessionmaker(bind=engine)
      self.stats = {}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
      spider = super(StateSenateDemocratPressReleasesSpider, cls).from_crawler(crawler, *args, **kwargs)
      crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
      return spider

    def spider_closed(self, spider):
      print(self.stats)

    def start_requests(self):
      yield scrapy.Request('http://sd09.senate.ca.gov/news/press-releases', meta={'legie_id':113})
      # session = self.Session()
      # for legie in session.query(Legislators).filter(and_(Legislators.party == 'Democrat', Legislators.house == 'Senate')):
        # if legie.name != 'Vacant':
          # yield scrapy.Request(legie.official_site_url + '/news/press-releases', meta={'legie_id':legie.id})

    def parse(self, response):
      legie_id = int(response.meta.get('legie_id', 0))
      if response.status == 404:
        self.stats[legie_id] = '404'
        if response.meta.get('existing_redirect', False):
          return
        else:
          # http://district21.cssrc.us/news/articles - need to deal with this
          yield scrapy.Request(response.request.url.replace('newsroom/releases', 'news/articles'), meta={'existing_redirect':True, legie_id:legie_id})

      self.stats[legie_id] = self.stats.get(legie_id,0) + 1
      for link in response.css('div.field-name-title a::attr(href)').extract():
        link = response.urljoin(link)
        yield scrapy.Request(link, callback=self.parse_press_release, meta={'legie_id':legie_id})

      next_page = response.css('ul.pagination li.next a::attr(href)').extract_first()
      if next_page is not None:
          next_page = response.urljoin(next_page)
          yield scrapy.Request(next_page, callback=self.parse, meta={'legie_id':legie_id})

    def parse_press_release(self, response):
      legie_id = response.meta.get('legie_id', 0)
      title = response.css('h1::text').extract_first()
      content = ' '.join([x.strip() for x in response.css('div.field-name-body *::text').extract() if x])
      timestamp = response.css('span.date-display-single::text').extract_first()
      timestamp = timestamp.replace('Monday, ', '').replace('Tuesday, ', '').replace('Wednesday, ', '').replace('Thursday, ', '').replace('Friday, ', '').replace('Saturday, ', '').replace('Sunday, ', '').replace(',', '')
      published = datetime.strptime(timestamp, "%B %d %Y")
      
      yield PressRelease(
        title = title,
        url = response.request.url,
        published = published,
        content = content,
        legislator = str(legie_id)
      )