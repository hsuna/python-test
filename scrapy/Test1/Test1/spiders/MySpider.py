import scrapy

class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = ["https://www.huya.com/l"]

    def parse(self, response):
        title_list = response.xpath('//*[@id="js-live-list"]/li/a[2]/text()').extract()
        name_list = response.xpath('//*[@id="js-live-list"]/li/span/span[1]/i/text()').extract()
        count_list = response.xpath('//*[@id="js-live-list"]/li/span/span[3]/i[2]/text()').extract()
        for i in range(1, len(title_list)):
            print(name_list[i-1], ': ', title_list[i-1], ' [', count_list[i-1], ']')