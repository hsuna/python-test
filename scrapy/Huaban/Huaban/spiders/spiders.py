# -*- coding: utf-8 -*-

import re
import json
import os
import winreg

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
from Huaban.items import HuabanItem
import logging

class HuabanSpider(CrawlSpider):
    name='huaban'
    limit=100
    base_url='http://login.meiwu.co/'
    cdn_url='http://img.hb.aicdn.com/'
    urlname=''

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

    def __init__(self, email='', password='', *args, **kwargs):
        super(HuabanSpider, self).__init__(*args, **kwargs)
        self.email = email
        self.password = password

    def start_requests(self):
        return [Request(
            url=self.get_url('login'),
            meta={'cookiejar': 1}, 
            dont_filter=False,
            callback=self.post_login
        )]  #重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数

    def post_login(self, response):
        data={
            '_ref': 'loginPage',
            'email': self.email,
            'password': self.password
        } #构造表单数据
        yield FormRequest(
            url=self.get_url('auth/'),
            headers={'X-Requested-With':'XMLHttpRequest'}, 
            method='POST',
            formdata=data, 
            dont_filter=False,
            callback=self.request_board
        )

    def request_board(self, response):
        data = json.loads(response.body)

        if 'user' in data:
            self.urlname = data['user']["urlname"]
            # 创建保存目录
            self.save_path = self.create_save_path(self.urlname)
            os.system('pause') #按任意键继续
            yield Request(
                url=self.get_url(self.urlname+'/pins/', '?limit='+str(self.limit)),
                headers={'X-Requested-With':'XMLHttpRequest'}, 
                callback=self.parse_pin
            )
        elif 'err' in data:
            logging.info('登录失败：['+data['msg']+']')
            print(data['msg'])
            os.system('pause')
        else:
            logging.info('登录失败：['+response.body+']')
            print(data)
            os.system('pause')

    def parse_pin(self, response):
        data = json.loads(response.body)
        pins = data["user"]["pins"]
        max = 0

        for pin in pins:
            pin_id = pin["pin_id"]
            max = max if int(pin_id) < max else int(pin_id)
            
            item = HuabanItem()
            item["savePath"] = self.save_path
            item["imgDir"] = pin["board"]["title"]
            item["imgName"] = str(pin["file_id"])
            item["imgType"] = pin["file"]["type"]
            item["imgUrl"] = self.cdn_url+pin["file"]["key"]
            yield item

        if len(pins)>=self.limit:
            yield Request(
                url=self.get_url(self.urlname+'/pins/', '?limit='+str(self.limit)+'&max='+str(max)),
                headers={'X-Requested-With':'XMLHttpRequest'}, 
                callback=self.parse_pin
            )

    def create_save_path(self, dirname):
        path = os.path.join(self.get_desktop(), self.name, dirname).strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        logging.info('文件将保存在['+path+']目录下')
        print('文件将保存在['+path+']目录下, 请保证该目录所在硬盘下有足够的空间！！！')
        return path

    def get_url(self, path, query=''):
        return self.base_url + path + query

    def get_desktop(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]