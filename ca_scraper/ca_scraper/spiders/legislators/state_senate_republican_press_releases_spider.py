import scrapy
from sqlalchemy.orm import sessionmaker
from ca_scraper.models import Legislators, db_connect, create_articles_table
from datetime import datetime
from sqlalchemy import and_
import time
from ca_scraper.items import PressRelease

class StateSenateRepublicanPressReleasesSpider(scrapy.Spider):
    name = 'state_senate_republican_press_releases'
    def __init__(self):
      engine = db_connect()
      create_articles_table(engine)
      self.Session = sessionmaker(bind=engine)
    def start_requests(self):
      session = self.Session()
      for legie in session.query(Legislators).filter(and_(Legislators.party == 'Republican', Legislators.house == 'Senate')):
        if legie.name != 'Vacant':
          yield scrapy.Request(legie.official_site_url + '/newsroom/releases', meta={'legie_id':legie.id})
      # test = 'https://a02.asmdc.org/'
      # yield scrapy.Request(test + 'press-releases', callback=self.parse, meta={'legie_id':77})
    def parse(self, response):
      legie_id = response.meta.get('legie_id', 0)
      if response.status == 404 and not response.meta.get('existing_redirect', False):
        print('********* REDIRECT *********')
        print(response.request.url)
        yield scrapy.Request(response.request.url.replace('newsroom/releases', 'news/articles'), meta={existing_redirect:True, legie_id:legie_id})

      for press_release in response.css('div#block-system-main div.view-Articles div.views-row'):
        link = response.urljoin(press_release.css('div.field-name-title h3 a::attr(href)').extract_first())
        print(link)
        yield scrapy.Request(link, callback=self.parse_press_release, meta={'legie_id':legie_id})

      next_page = response.css('li.pager-next a::attr(href)').extract_first()
      if next_page is not None:
          next_page = response.urljoin(next_page)
          yield scrapy.Request(next_page, callback=self.parse, meta={'legie_id':legie_id})

    def parse_press_release(self, response):
      legie_id = response.meta.get('legie_id', 0)
      title = response.css('h1#page-title::text').extract_first()
      content = ' '.join([x.strip() for x in response.css('section#main-content div.field-name-body *::text').extract() if x])
      timestamp = response.css('span.date-display-single::attr(content)').extract_first()
      timestamp_extracted = time.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S")
      published = datetime(*timestamp_extracted[:6])
      yield PressRelease(
        title = title,
        url = response.request.url,
        published = published,
        content = content,
        legislator = str(legie_id)
      )