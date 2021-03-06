# -*- coding:utf-8 -*-

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Mongo.items import DoubanmovieItem


class MovieSpider(CrawlSpider):
    name = "douban"
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    rules = [
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250\?start=\d+.'))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+')), callback="parse_item"),
    ]

    def parse_item(self, response):
        sel = Selector(response)
        item = DoubanmovieItem()
        item['name'] = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year'] = sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score'] = sel.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()').extract()
        item['director'] = sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['classification'] = sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor'] = sel.xpath('//*[@id="info"]/span[3]/span[2]/a[@rel="v:starring"]/text()').extract()
        return item
