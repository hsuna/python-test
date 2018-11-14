# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    # 房屋户型
    mode = scrapy.Field()
    # 房屋单价
    price = scrapy.Field()
    # 房屋位置
    location = scrapy.Field()
    area = scrapy.Field()
    # 房屋面积
    floor = scrapy.Field()
    # 楼龄
    age = scrapy.Field()
    
    district = scrapy.Field()
