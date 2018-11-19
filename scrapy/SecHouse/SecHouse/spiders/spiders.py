# -*- coding: utf-8 -*-

import re

from pymongo import MongoClient

import scrapy
from scrapy.conf import settings
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from SecHouse.items import HouseItem,HouseItem2,HouseItem3

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


class HouseSpider2(CrawlSpider):
    name = 'house2'
    start_urls = ['https://m.anjuke.com/gz/sale/']
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Eanguage': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        }
    }
    #start_urls = ['http://192.168.16.84:5500/test/house/3.html']
   
    def start_requests(self):
        for i in range(11, 20):
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
    #def parse(self, response):
        selector = Selector(response)

        # 存放房子信息
        item = HouseItem2()
        
        housebasic = selector.xpath('//div[@class="house-info-content"]')
        if housebasic.extract()[0]:
            item['title'          ] = housebasic.xpath('normalize-space(./div[@class="house-address"]/text())').extract()[0]
            item['tolprice'       ] = housebasic.xpath('normalize-space(./div[@class="house-data"]/span[1]/text())').extract()[0]
            item['mode'           ] = housebasic.xpath('normalize-space(./div[@class="house-data"]/span[2]/text())').extract()[0]
            item['area'           ] = housebasic.xpath('normalize-space(./div[@class="house-data"]/span[3]/text())').extract()[0]

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
            try:
                item['traffic'        ] = houseinfo[11].xpath('normalize-space(./text())').extract()[0]
            except Exception as e:
                item['traffic'        ] = ''
            #print(item)
            return item



class HouseSpider3(CrawlSpider):
    name = 'house3'
    start_urls = ['https://m.anjuke.com/gz/sale/']
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Eanguage': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        }
    }
    dont_redirect = True
    handle_httpstatus_list = [302]

    def start_requests(self):
        client = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = client[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

        for i in range(1, 200):
            url = 'https://m.anjuke.com/gz/sale/?from=anjuke_home&page='+str(i)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        selector = Selector(response)
        urls = selector.xpath('//a[contains(@class, "house-item")]/@href').extract()
        
        for url in urls:
            house_id = re.match(r'.*/gz/sale/(\w*).*', url, re.M|re.I)
            if str(house_id) == 'None':
                pass
            else:
                result = self.collection.find_one({'house_id': house_id.group(1)})
                if result:
                    pass
                else:
                    yield scrapy.Request(url, callback=self.parse_item)
    

    def parse_item(self, response):
        selector = Selector(response)
        housebasic = selector.xpath('//div[@class="house-info-content"]')
        if len(housebasic.extract()) > 0:
            # 存放房子信息
            item = HouseItem3()
            item['house_id'       ] = re.match(r'.*/gz/sale/(\w*).*', response.url, re.M|re.I).group(1)
            item['title'          ] = housebasic.xpath('normalize-space(./div[@class="house-address"]/text())').extract()[0]
            item['tolprice'       ] = housebasic.xpath('normalize-space(./div[@class="house-data"]/span[1]/text())').extract()[0]
            item['mode'           ] = housebasic.xpath('normalize-space(./div[@class="house-data"]/span[2]/text())').extract()[0]
            item['area'           ] = housebasic.xpath('normalize-space(./div[@class="house-data"]/span[3]/text())').extract()[0]

            houseinfo = selector.xpath('//ul[@class="info-list"]/li')
            for i, info in enumerate(houseinfo):
                item['price'          ] = info.xpath('normalize-space(./text())').extract()[0] if i==0 else ''
                item['orientation'    ] = info.xpath('normalize-space(./text())').extract()[0] if i==1 else ''
                item['floor'          ] = info.xpath('normalize-space(./text())').extract()[0] if i==2 else ''
                item['decorate'       ] = info.xpath('normalize-space(./text())').extract()[0] if i==3 else ''
                item['built'          ] = info.xpath('normalize-space(./text())').extract()[0] if i==4 else ''
                item['house_type'     ] = info.xpath('normalize-space(./text())').extract()[0] if i==5 else ''
                item['agelimit'       ] = info.xpath('normalize-space(./text())').extract()[0] if i==6 else ''
                item['elevator'       ] = info.xpath('normalize-space(./text())').extract()[0] if i==7 else ''
                item['only'           ] = info.xpath('normalize-space(./text())').extract()[0] if i==8 else ''
                item['budget'         ] = info.xpath('normalize-space(./a/text())').extract()[0] if i==9 else ''
                item['district'       ] = info.xpath('normalize-space(./a/text())').extract()[0] if i==10 else ''
                item['traffic'       ] = info.xpath('normalize-space(./text())').extract()[0] if i==11 else ''
            #print(item)
            return item