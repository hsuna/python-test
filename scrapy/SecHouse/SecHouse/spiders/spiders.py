from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from SecHouse.items import HouseItem

class HouseSpider(CrawlSpider):
    name = 'house'
    start_urls = ['https://guangzhou.anjuke.com/sale/']
    rules = [
        Rule(LinkExtractor(allow=(r'https://guangzhou.anjuke.com/sale/p\d+'))),
        Rule(LinkExtractor(allow=(r'https://guangzhou.anjuke.com/prop/view/\w+')), callback="parse_item"),
        
    ]

    def parse_item(self, response):
        selector = scrapy.Selector(response)
        # 存放房子信息
        item = HouseItem()