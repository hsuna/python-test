# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

from scrapy.exceptions import DropItem
from scrapy.conf import settings

import logging


class MongoPipeline(object):
    def process_item(self, item, spider):
        return item

class DoubanmoviePipeline(object):
    def __init__(self):
        client = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = client[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing %s of blogpost from %s"%(data,item['url']))
        if valid:
            new_movie=[{
                "name":item['name'][0],
                "year":item['year'][0],
                "score":item['score'][0],
                "director":item['director'],
                "classification":item['classification'],
                "actor":item['actor']
            }]
            self.collection.insert(new_movie)
            logging.debug("Item wrote to MongoDB database %s/%s"%(settings['MONGODB_DB'],settings['MONGODB_COLLECTION']))
        return item
