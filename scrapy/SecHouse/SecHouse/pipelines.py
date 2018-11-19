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
        self.collection = db[settings['MONGODB_COLLECTION']]
    
    def process_item(self, item, spider):
        valid=True
        for data in item:
            if not data:
                valid=False
                raise DropItem('Missing{0}!'.format(data))
        if valid and self.valid_item(item):
            self.collection.insert(dict(item))
            logging.debug("Item wrote to MongoDB database %s/%s"%(settings['MONGODB_DB'],settings['MONGODB_COLLECTION']))
        return item
    
    def valid_item(self, item):
        return True

class MongoPipeline2(MongoPipeline):
    def valid_item(self, item):
        results = self.collection.find_one({'house_id': item['house_id']})
        if result:
            return False
        else:
            return True