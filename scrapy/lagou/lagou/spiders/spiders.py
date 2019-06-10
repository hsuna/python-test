# -*- coding: utf-8 -*-

import json
import time

import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest

from lagou.items import LagouItem


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    start_urls = ['https://www.lagou.com/']
    base_url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false'
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "",
            "Host": "www.lagou.com",
            "Origin": "https://www.lagou.com",
            "Referer": "https://www.lagou.com/jobs/list_web%E5%89%8D%E7%AB%AF?px=default&city=%E5%85%A8%E5%9B%BD",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "X-Anit-Forge-Code": "0",
            "X-Anit-Forge-Token": "None",
            "X-Requested-With": "XMLHttpRequest"
        }
    }

    def start_requests(self):
        for i in [28]:
        #for i in range(1, 31):
            formdata = {'first':'false', 'pn':str(i), 'kd':'web前端'}
            yield FormRequest(url=self.base_url, callback=self.parse_model, formdata=formdata)

    def parse_model(self, response):
        jsonBody = json.loads(response.body.decode())
        if jsonBody['success']:
            results = jsonBody['content']['positionResult']['result']
            items=[]
            for result in results:
                item = LagouItem()
                item['page'] = jsonBody['content']['pageNo']
                item['name'] = result['companyFullName']
                item['location'] = result['city']
                item['position'] = result['positionName']
                item['exprience'] = result['workYear']
                item['money'] = result['salary']
                items.append(item)
            return items
        else:
            print(jsonBody['msg'], jsonBody['clientIp'])


class IpSpider(scrapy.Spider):
    name = 'ip'
    start_urls = ['http://2018.ip138.com/']
    allowed_domains = []

    def start_requests(self):
        url = 'http://2018.ip138.com/ic.asp'
        #for i in range(4):
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        print(sel.xpath('//center/text()').extract())