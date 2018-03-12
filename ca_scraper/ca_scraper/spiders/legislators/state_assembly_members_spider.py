import scrapy
from ca_scraper.items import Legislator
from datetime import datetime

class StateAssemblyMembersSpider(scrapy.Spider):
    name = 'state_assembly_members'

    start_urls = ['http://assembly.ca.gov/assemblymembers']

    def parse(self, response):
      print('what is going on?')
      for member in response.css('#block-views-view-members-block-1 tbody tr'):
        name = member.css('td.views-field-field-member-lname-sort a::text').extract_first(default='').strip()
        name = " ".join(name.split(", ")[::-1])
        legie = Legislator(
            state = 'CA',
            house = 'Assembly',
            district = member.css('td:nth-child(2)::text').extract_first(default='').strip(),
            party = member.css('td:nth-child(3)::text').extract_first(default='').strip(),
            name = name,
            official_site_url = member.css('td:nth-child(1) a::attr(href)').extract_first(default='').strip(),
            img_src = member.css('img::attr(src)').extract_first(default='').strip(),
        )
        print(legie)
        yield legie