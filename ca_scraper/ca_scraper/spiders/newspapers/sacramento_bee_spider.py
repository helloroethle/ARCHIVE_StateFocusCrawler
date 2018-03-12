import scrapy
import feedparser
from ca_scraper.items import Article
from datetime import datetime

class SacramentoBeeSpider(scrapy.Spider):
    name = 'sacramento_bee'

    start_urls = ['http://www.sacbee.com/news/?widgetName=rssfeed&widgetContentId=713546&getXmlFeed=true']


    def parse_feed(self, feed):
        data = feedparser.parse(feed)
        return data

    def parse(self, response):
        # parse downloaded content with feedparser (NOT re-downloading with feedparser)
        feed = self.parse_feed(response.body)
        if feed:
            for entry in feed.entries:
                item = {
                    # item entry data
                    'url': entry.link,
                    'title': entry.title,
                    'date': entry.published,
                }
                yield scrapy.Request(entry.link, callback=self.parse_article, meta=item)

    def parse_article(self, response):
        selector = '.pb-f-article-body'
        text = ' '.join([x.strip() for x in response.css('div#content-body *::text').extract() if x])
        author = ' '.join([x.strip() for x in response.css('div.byline *::text').extract() if x])
        yield Article(
            title = response.meta.get('title', ''),
            url = response.meta.get('url', ''),
            published = response.meta.get('date', datetime.now()),
            content = text,
            author = author,
            source = 'Sacramento Bee'
        )