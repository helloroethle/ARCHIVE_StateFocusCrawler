import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ca_scraper.spiders.newspapers.contra_costa_times_spider import ContraCostaTimesSpider
from ca_scraper.spiders.newspapers.la_times_spider import LATimesSpider
from ca_scraper.spiders.newspapers.mercury_news_spider import MercuryNewsSpider
from ca_scraper.spiders.newspapers.oc_register_spider import OCRegisterSpider
from ca_scraper.spiders.newspapers.press_enterprise_spider import PressEnterpriseSpider
from ca_scraper.spiders.newspapers.sacramento_bee_spider import SacramentoBeeSpider
from ca_scraper.spiders.newspapers.san_diego_union_tribune_spider import SanDiegoUnionTribuneSpider
from ca_scraper.spiders.newspapers.san_francisco_chronicle_spider import SanFranciscoChronicleSpider


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