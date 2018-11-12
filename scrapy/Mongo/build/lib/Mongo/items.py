# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MongoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DoubanmovieItem(scrapy.Item):
     # define the fields for your item here like:
    name = scrapy.Field()
    year = scrapy.Field()
    score = scrapy.Field()
    director = scrapy.Field()
    classification = scrapy.Field()
    actor = scrapy.Field()