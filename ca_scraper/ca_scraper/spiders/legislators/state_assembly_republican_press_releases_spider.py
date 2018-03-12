import scrapy
from sqlalchemy.orm import sessionmaker
from ca_scraper.models import Articles, Legislators, db_connect, create_articles_table
from datetime import datetime
from sqlalchemy import and_

class StateAssemblyRepublicanPressReleasesSpider(scrapy.Spider):
    name = 'state_assembly_republican_press_releases'
    def __init__(self):
      engine = db_connect()
      create_articles_table(engine)
      self.Session = sessionmaker(bind=engine)
    def start_requests(self):
      session = self.Session()
      for legie in session.query(Legislators).filter(and_(Legislators.party == 'Democrat', Legislators.house == 'Assembly')):
        print(legie.name)
        yield scrapy.Request(legie.official_site_url)
    def parse(self, response):
      print('parsing')
      # for member in response.css('#block-views-view-members-block-1 tbody tr'):
      #   name = member.css('td.views-field-field-member-lname-sort a::text').extract_first(default='').strip()
      #   name = " ".join(name.split(", ")[::-1])
      #   legie = Legislator(
      #     state = 'CA',
      #     district = member.css('td:nth-child(2)::text').extract_first(default='').strip(),
      #     party = member.css('td:nth-child(3)::text').extract_first(default='').strip(),
      #     name = name,
      #     official_site_url = member.css('td:nth-child(1) a::attr(href)').extract_first(default='').strip(),
      #     img_src = member.css('img::attr(src)').extract_first(default='').strip(),
      #   )
      yield 'cool'
