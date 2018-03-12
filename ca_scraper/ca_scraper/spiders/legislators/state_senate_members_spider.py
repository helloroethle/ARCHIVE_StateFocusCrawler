import scrapy
from ca_scraper.items import Legislator
from datetime import datetime

class StateSenateMembersSpider(scrapy.Spider):
    name = 'state_senate_members'

    start_urls = ['http://senate.ca.gov/senators']

    def parse(self, response):
      for member in response.css('#block-views-senator-roster-block div.views-row'):
         name = member.css('div.views-field-field-senator-last-name h3::text').extract_first()
         party = name[len(name)-2]
         if(party == 'D'):
            party = 'Democrat';
         else:
            party = 'Republican';
         name = name[0:len(name)-4]
         legie = Legislator(
            state = 'CA',
            house = 'Senate',
            district = ' '.join([x.strip() for x in member.css('div.views-field-field-senator-district *::text').extract() if x]).replace('District', '').strip(),
            party = party,
            name = name,
            official_site_url = member.css('div.views-field-field-senator-weburl a::attr(href)').extract_first(default='').strip(),
            img_src = member.css('div.views-field-field-senator-photo img::attr(src)').extract_first(default='').strip()
         )
         yield legie