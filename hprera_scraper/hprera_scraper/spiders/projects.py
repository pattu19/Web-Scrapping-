import scrapy


class ProjectsSpider(scrapy.Spider):
    name = "projects"
    allowed_domains = ["hprera.nic.in"]
    start_urls = ["https://hprera.nic.in"]

    def parse(self, response):
        pass
