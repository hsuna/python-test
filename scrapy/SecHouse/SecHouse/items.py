# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    # 所属小区
    district = scrapy.Field()
    # 房屋户型
    mode = scrapy.Field()
    # 房屋单价
    price = scrapy.Field()
    # 所在位置
    location = scrapy.Field()
    # 建筑面积
    area = scrapy.Field()
    # 参考首付
    downpayment = scrapy.Field()
    # 建造年代
    built = scrapy.Field()
    # 房屋朝向
    orientation = scrapy.Field()
    # 参考月供
    payment = scrapy.Field()
    # 房屋类型
    house_type = scrapy.Field()
    # 所在楼层
    floor = scrapy.Field()
    # 装修程度
    decorate = scrapy.Field()
    # 产权年限
    age = scrapy.Field()
    # 配套电梯
    elevator = scrapy.Field()
    # 房本年限
    agelimit = scrapy.Field()
    # 产权性质
    property_right = scrapy.Field()
    # 唯一住房
    only = scrapy.Field()


class HouseItem2(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 房屋总价
    tolprice = scrapy.Field()
    # 房屋户型
    mode = scrapy.Field()
     # 建筑面积
    area = scrapy.Field()

    # 房屋单价
    price = scrapy.Field()
    # 房屋朝向
    orientation = scrapy.Field()
    # 所在楼层
    floor = scrapy.Field()
    # 装修程度
    decorate = scrapy.Field()
    # 建造年代
    built = scrapy.Field()
    # 房屋类型
    house_type = scrapy.Field()
    # 房本年限
    agelimit = scrapy.Field()
    # 配套电梯
    elevator = scrapy.Field()
    # 唯一住房
    only = scrapy.Field()
    # 参考月供
    budget = scrapy.Field()
    # 所属小区
    district = scrapy.Field()
    # 交通
    traffic = scrapy.Field()


class HouseItem3(scrapy.Item):
    # ID
    house_id = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 房屋总价
    tolprice = scrapy.Field()
    # 房屋户型
    mode = scrapy.Field()
     # 建筑面积
    area = scrapy.Field()

    # 房屋单价
    price = scrapy.Field()
    # 房屋朝向
    orientation = scrapy.Field()
    # 所在楼层
    floor = scrapy.Field()
    # 装修程度
    decorate = scrapy.Field()
    # 建造年代
    built = scrapy.Field()
    # 房屋类型
    house_type = scrapy.Field()
    # 房本年限
    agelimit = scrapy.Field()
    # 配套电梯
    elevator = scrapy.Field()
    # 唯一住房
    only = scrapy.Field()
    # 参考月供
    budget = scrapy.Field()
    # 所属小区
    district = scrapy.Field()
    # 交通
    traffic = scrapy.Field()