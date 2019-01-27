# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class HuabanItem(scrapy.Item):
    # define the fields for your item here like:
    # 目录名
    imgDir = scrapy.Field()
    # 类型
    imgType = scrapy.Field()
    # 图片名
    imgName = scrapy.Field()
    # 图片链接
    imgUrl = scrapy.Field()
    