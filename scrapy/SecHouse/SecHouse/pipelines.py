# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

from scrapy.conf import settings

import logging

class SechousePipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    def __init__(self):
        client = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = client[settings['MONGODB_DB']]
        self.pageColl = db[settings['MONGODB_COLLECTION_PAGE']]
        self.houseColl = db[settings['MONGODB_COLLECTION_HOUSE']]
    
    def process_item(self, item, spider):
        valid=True
        for data in item:
            if not data:
                valid=False
                raise DropItem('Missing{0}!'.format(data))
        if valid:
            self.collection.insert(dict(item))
            logging.debug("Item wrote to MongoDB database %s/%s"%(settings['MONGODB_DB'],settings['MONGODB_COLLECTION']))
        return item

class MongoPipeline2(MongoPipeline):

    def process_item(self, item, spider):
        valid=True
        for data in item:
            if not data:
                valid=False
                raise DropItem('Missing{0}!'.format(data))
        if valid:

    def process_PageItem(self, item):
        try:
            self.pageColl.insert(dict(item))
            print("记录页面%s"%item["page"])
        except Exception:
            print("页面《%s》已经爬过，跳过"%item["page"])

    def process_HouseItem(self, item):
        try:
            self.houseColl.insert(dict(item))
            print("插入数据[%s]"%item["id"])
        except Exception:
            print("数据[%s]已经存在"%item["id"])