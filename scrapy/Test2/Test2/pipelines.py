# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

import pymysql
from twisted.enterprise import adbapi

class DoubanPipeline(object):
    def __init__(self):
        # 打开文件
        self.file = open('data.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 读取item中的数据
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 写入文件
        self.file.write(line)
        # 返回item
        return item

    # 该方法在spider被开启时被调用。
    def open_spider(self, spider):
        pass

    # 该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        self.file.close()

class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['img_url'])

    def item_completed(self, results, item, info):
        img_url = [x['path'] for ok, x in results if ok]

        if not img_url:
            raise DropItem("Item contains no images")

        item['img_url'] = img_url
        return item


class MySqlPipeline(object):
    def __init__(self):

        # 定义链接的数据库的相关信息
        self.dbpool = adbapi.ConnectionPool('pymysql', 
            host='127.0.0.1',
            db='python',
            user='root',
            passwd='123456',
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8',
            use_unicode=False)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    def _conditional_insert(self, tx, item):
        # print item['name']
        sql = "insert into doubanmovie(name, info, rating, num, quote, img_url) values(%s,%s,%s,%s,%s,%s)"
        params = (item["name"], item["info"], item["rating"], item["num"], item["quote"], item["img_url"])
        #执行sql语句
        tx.execute(sql, params)
 
 
    def _handle_error(self, failure, item, spider):
        print('--------------database operation exception!!-----------------')
        print('-------------------------------------------------------------')
        print(failure)