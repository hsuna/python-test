# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    page = Field()
    name = Field()
    location = Field()
    position = Field()
    exprience = Field()
    money = Field()
