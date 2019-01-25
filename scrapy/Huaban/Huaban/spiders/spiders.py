# -*- coding: utf-8 -*-

import re
import json

from urllib.parse import urlparse, urlunparse

import scrapy
from scrapy.conf import settings
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
from Huaban.items import HuabanItem

INPUT_EMAIL='xxxxxxx'
INPUT_PASSWORD='xxxxxxxx'

class HuabanSpider(CrawlSpider):
    name='huaban'
    limit=100
    custom_settings={
        "DOWNLOAD_DELAY": .5
    }
    headers={
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "60",
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "login.meiwu.co",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "X-Request": "JSON",
        "X-Requested-With": "XMLHttpRequest",
    }

    def start_requests(self):
        return [Request(
            url="http://login.meiwu.co/login",
            meta={'cookiejar': 1}, 
            dont_filter=False,
            callback=self.post_login
        )]  #重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数

    def post_login(self, response):
        data={
            '_ref': 'loginPage',
            'email': INPUT_EMAIL,
            'password': INPUT_PASSWORD
        } #构造表单数据
        yield FormRequest(
            url='http://login.meiwu.co/auth/',
            method='POST',
            formdata=data, 
            dont_filter=False,
            callback=self.request_board
            
        )

    def request_board(self, response):
        yield Request(
            url=self.get_urlpath(response.url, ['limit='+str(self.limit)]),
            headers={'X-Requested-With':'XMLHttpRequest'}, 
            callback=self.parse_board
        )
        
    def parse_board(self, response):
        data = json.loads(response.body)
        boards = data["user"]["boards"]
        max = 0

        print(response.url)

        for board in boards:
            board_id = board["board_id"]
            max = max if int(board_id) < max else int(board_id)
            yield Request(
                url=self.get_urlpath('http://login.meiwu.co/boards/'+str(board_id), ['limit='+str(self.limit), 'wfl=1']),
                headers={'X-Requested-With':'XMLHttpRequest'}, 
                callback=self.parse_pin
            )
        
        if len(boards)>=self.limit:
            yield Request(
                url=self.get_urlpath(response.url, ['limit='+str(self.limit), 'max='+str(max)]),
                headers={'X-Requested-With':'XMLHttpRequest'}, 
                callback=self.parse_board
            )

    def parse_pin(self, response):
        data = json.loads(response.body)
        pins = data["board"]["pins"]
        title = data["board"]["title"]
        max = 0

        for pin in pins:
            pin_id = pin["pin_id"]
            max = max if int(pin_id) < max else int(pin_id)
            
            item = HuabanItem()
            item["imgDir"] = title
            item["imgName"] = str(pin["file_id"])
            item["imgType"] = pin["file"]["type"]
            item["imgUrl"] = 'http://img.hb.aicdn.com/'+pin["file"]["key"]
            yield item

        if len(pins)>=self.limit:
            yield Request(
                url=self.get_urlpath(response.url, ['limit='+str(self.limit), 'wfl=1', 'max='+str(max)]),
                headers={'X-Requested-With':'XMLHttpRequest'}, 
                callback=self.parse_pin
            )

    def get_urlpath(self, url, query):
        r = urlparse(url)
        return urlunparse([r.scheme, r.netloc, r.path, '', ('&').join(query), ''])



class HuabanSpider2(CrawlSpider):
    name='huaban2'
    limit=100
    custom_settings={
        "DOWNLOAD_DELAY": .5
    }
    headers={
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "60",
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "login.meiwu.co",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "X-Request": "JSON",
        "X-Requested-With": "XMLHttpRequest",
    }

    def start_requests(self):
        return [Request(
            url="http://login.meiwu.co/login",
            meta={'cookiejar': 1}, 
            dont_filter=False,
            callback=self.post_login
        )]  #重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数

    def post_login(self, response):
        data={
            '_ref': 'loginPage',
            'email': INPUT_EMAIL,
            'password': INPUT_PASSWORD
        } #构造表单数据
        yield FormRequest(
            url='http://login.meiwu.co/auth/',
            method='POST',
            formdata=data, 
            dont_filter=False,
            callback=self.request_board
        )

    def request_board(self, response):
        yield Request(
            url=self.get_urlpath(response.url+'/pins/', ['limit='+str(self.limit)]),
            headers={'X-Requested-With':'XMLHttpRequest'}, 
            callback=self.parse_pin
        )

    def parse_pin(self, response):
        data = json.loads(response.body)
        pins = data["user"]["pins"]
        max = 0

        for pin in pins:
            pin_id = pin["pin_id"]
            max = max if int(pin_id) < max else int(pin_id)
            
            item = HuabanItem()
            item["imgDir"] = pin["board"]["title"]
            item["imgName"] = str(pin["file_id"])
            item["imgType"] = pin["file"]["type"]
            item["imgUrl"] = 'http://img.hb.aicdn.com/'+pin["file"]["key"]
            yield item

        if len(pins)>=self.limit:
            yield Request(
                url=self.get_urlpath(response.url, ['limit='+str(self.limit), 'max='+str(max)]),
                headers={'X-Requested-With':'XMLHttpRequest'}, 
                callback=self.parse_pin
            )

    def get_urlpath(self, url, query):
        r = urlparse(url)
        return urlunparse([r.scheme, r.netloc, r.path, '', ('&').join(query), ''])