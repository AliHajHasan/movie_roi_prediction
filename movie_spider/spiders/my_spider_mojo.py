import scrapy


class MySpiderMojoSpider(scrapy.Spider):
    name = "my_spider_mojo"
    allowed_domains = ["www.boxofficemojo.com"]
    start_urls = ["https://www.boxofficemojo.com/"]

    def parse(self, response):
        pass
