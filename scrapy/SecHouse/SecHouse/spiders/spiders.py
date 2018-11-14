# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from SecHouse.items import HouseItem

class HouseSpider(CrawlSpider):
    name = 'house'
    start_urls = ['https://guangzhou.anjuke.com/prop/view/A1484458022']
    #start_urls = ['https://guangzhou.anjuke.com/']
    #rules = [
    #    Rule(LinkExtractor(allow=(r'https://guangzhou.anjuke.com/sale/p\d+'))),
    #    Rule(LinkExtractor(allow=(r'https://guangzhou.anjuke.com/prop/view/\w+')), callback="parse_item"),
    #    
    #]

    def parse(self, response):
    # def parse_item(self, response):
        selector = Selector(response)
        houseinfo = selector.xpath('//li[@class="houseInfo-detail-item"]')

        # 存放房子信息
        item = HouseItem()
        item['district'] = houseinfo.xpath('.//div[2]/a/text()').extract()
        item['mode'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['price'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['location'] = houseinfo.xpath('.//div[2]/p/text()').extract()
        item['area'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['downpayment'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['built'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['orientation'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['payment'] = houseinfo.xpath('.//div[2]/span/text()').extract()
        item['house_type'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['floor'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['decorate'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['age'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['elevator'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['agelimit'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['property_right'] = houseinfo.xpath('.//div[2]/text()').extract()
        item['only'] = houseinfo.xpath('.//div[2]/text()').extract()
        print(item)