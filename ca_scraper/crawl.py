import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ca_scraper.spiders.contra_costa_times_spider import ContraCostaTimesSpider
from ca_scraper.spiders.la_times_spider import LATimesSpider
from ca_scraper.spiders.mercury_news_spider import MercuryNewsSpider
from ca_scraper.spiders.oc_register_spider import OCRegisterSpider
from ca_scraper.spiders.press_enterprise_spider import PressEnterpriseSpider
from ca_scraper.spiders.sacramento_bee_spider import SacramentoBeeSpider
from ca_scraper.spiders.san_diego_union_tribune_spider import SanDiegoUnionTribuneSpider
from ca_scraper.spiders.san_francisco_chronicle_spider import SanFranciscoChronicleSpider


process = CrawlerProcess(get_project_settings())
process.crawl(ContraCostaTimesSpider)
process.crawl(LATimesSpider)
process.crawl(MercuryNewsSpider)
process.crawl(OCRegisterSpider)
process.crawl(PressEnterpriseSpider)
process.crawl(SacramentoBeeSpider)
process.crawl(SanDiegoUnionTribuneSpider)
process.crawl(SanFranciscoChronicleSpider)
process.start() # the script will block here until all crawling jobs are finished