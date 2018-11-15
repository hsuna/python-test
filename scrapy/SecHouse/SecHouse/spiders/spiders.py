# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from SecHouse.items import HouseItem

class HouseSpider(CrawlSpider):
    name = 'house'
    start_urls = ['https://guangzhou.anjuke.com/']
    rules = [
        Rule(LinkExtractor(allow=(r'https://guangzhou.anjuke.com/sale/p\d+'))),
        Rule(LinkExtractor(allow=(r'https://guangzhou.anjuke.com/prop/view/\w+')), callback="parse_item"),
        
    ]

    # def parse(self, response):
    def parse_item(self, response):
        selector = Selector(response)
        houseinfo = selector.xpath('//li[@class="houseInfo-detail-item"]')

        # 存放房子信息
        item = HouseItem()
        item['district'       ] = houseinfo[0 ].xpath('normalize-space(.//div[2]/a/text())').extract()[0]
        item['mode'           ] = houseinfo[1 ].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['price'          ] = houseinfo[2 ].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['location'       ] = houseinfo[3 ].xpath('.//div[2]/p').xpath('normalize-space(string(.))').extract()[0]
        item['area'           ] = houseinfo[4 ].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['downpayment'    ] = houseinfo[5 ].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['built'          ] = houseinfo[6 ].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['orientation'    ] = houseinfo[7 ].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['payment'        ] = houseinfo[8 ].xpath('normalize-space(.//div[2]/span/text())').extract()[0]
        item['house_type'     ] = houseinfo[9 ].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['floor'          ] = houseinfo[10].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['decorate'       ] = houseinfo[11].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['age'            ] = houseinfo[12].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['elevator'       ] = houseinfo[13].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['agelimit'       ] = houseinfo[14].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['property_right' ] = houseinfo[15].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['only'           ] = houseinfo[16].xpath('normalize-space(.//div[2]/text())').extract()[0]
        return item