import scrapy


class MySpiderNumbersSpider(scrapy.Spider):
    name = "my_spider_numbers"
    allowed_domains = ["www.the-numbers.com"]
    start_urls = ["https://www.the-numbers.com/"]

    def parse(self, response):
        pass
