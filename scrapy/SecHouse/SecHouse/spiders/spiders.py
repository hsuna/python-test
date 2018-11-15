# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from SecHouse.items import HouseItem,MHouseItem

class HouseSpider(CrawlSpider):
    name = 'house'
    start_urls = ['https://guangzhou.anjuke.com/']
    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "RANDOM_DELAY": 3
    }
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
        item['district'       ] = houseinfo[0].xpath('normalize-space(.//div[2]/a/text())').extract()[0]
        item['mode'           ] = houseinfo[1].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['price'          ] = houseinfo[2].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['location'       ] = houseinfo[3].xpath('.//div[2]/p').xpath('normalize-space(string(.))').extract()[0]
        item['area'           ] = houseinfo[4].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['downpayment'    ] = houseinfo[5].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['built'          ] = houseinfo[6].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['orientation'    ] = houseinfo[7].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['payment'        ] = houseinfo[8].xpath('normalize-space(.//div[2]/span/text())').extract()[0]
        item['house_type'     ] = houseinfo[9].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['floor'          ] = houseinfo[10].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['decorate'       ] = houseinfo[11].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['age'            ] = houseinfo[12].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['elevator'       ] = houseinfo[13].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['agelimit'       ] = houseinfo[14].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['property_right' ] = houseinfo[15].xpath('normalize-space(.//div[2]/text())').extract()[0]
        item['only'           ] = houseinfo[16].xpath('normalize-space(.//div[2]/text())').extract()[0]
        return item


class MobileHouseSpider(CrawlSpider):
    name = 'mhouse'
    start_urls = ['https://m.anjuke.com/gz/sale/']
   
    def start_requests(self):
        for i in range(1, 500):
            url = 'https://m.anjuke.com/gz/sale/?from=anjuke_home&page='+str(i)
            yield scrapy.Request(url, callback=self.parse_page, meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [302]
            })

    def parse_page(self, response):
        selector = Selector(response)
        urls = selector.xpath('//a[contains(@class, "house-item")]/@href').extract()
        
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_item, meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [302]
            })

    def parse_item(self, response):
        selector = Selector(response)

        # 存放房子信息
        item = MHouseItem()
        
        housebasic = selector.xpath('//div[@class="house-info-content"]')
        item['title'          ] = housebasic.xpath('normalize-space(.//div[@class="house-address"]/text())').extract()[0]
        item['tolprice'       ] = housebasic.xpath('normalize-space(.//div[@class="house-data"]/span[1]/text())').extract()[0]
        item['mode'           ] = housebasic.xpath('normalize-space(.//div[@class="house-data"]/span[2]/text())').extract()[0]
        item['area'           ] = housebasic.xpath('normalize-space(.//div[@class="house-data"]/span[3]/text())').extract()[0]

        houseinfo = selector.xpath('//ul[@class="info-list"]/li')
        item['price'          ] = houseinfo[0].xpath('normalize-space(./text())').extract()[0]
        item['orientation'    ] = houseinfo[1].xpath('normalize-space(./text())').extract()[0]
        item['floor'          ] = houseinfo[2].xpath('normalize-space(./text())').extract()[0]
        item['decorate'       ] = houseinfo[3].xpath('normalize-space(./text())').extract()[0]
        item['built'          ] = houseinfo[4].xpath('normalize-space(./text())').extract()[0]
        item['house_type'     ] = houseinfo[5].xpath('normalize-space(./text())').extract()[0]
        item['agelimit'       ] = houseinfo[6].xpath('normalize-space(./text())').extract()[0]
        item['elevator'       ] = houseinfo[7].xpath('normalize-space(./text())').extract()[0]
        item['only'           ] = houseinfo[8].xpath('normalize-space(./text())').extract()[0]
        item['budget'         ] = houseinfo[9].xpath('normalize-space(./a/text())').extract()[0]
        item['district'       ] = houseinfo[10].xpath('normalize-space(./a/text())').extract()[0] + houseinfo[10].xpath('normalize-space(./text())').extract()[0]
        item['traffic'        ] = houseinfo[11].xpath('normalize-space(./text())').extract()[0]
        return item