import scrapy
from scrapy_splash import SplashRequest

class ProjectsSpider(scrapy.Spider):
    name = 'projects_spider'
    allowed_domains = ['hprera.nic.in']
    start_urls = ['https://hprera.nic.in/PublicDashboard']

    script = """
    function main(splash, args)
      splash.private_mode_enabled = false
      splash:go(args.url)
      splash:wait(2)
      return {
        html = splash:html()
      }
    end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                self.parse,
                endpoint='execute',
                args={'lua_source': self.script}
            )

    def parse(self, response):
        project_links = response.css('a[data-qs]::attr(href)').getall()[:6]
        self.logger.info(f'Found project links: {project_links}')
        for link in project_links:
            yield SplashRequest(
                response.urljoin(link),
                self.parse_project_details,
                endpoint='execute',
                args={'lua_source': self.script}
            )

    def parse_project_details(self, response):
        self.logger.info(f'Parsing project details for: {response.url}')
        gstin = response.css('span.mr-1.fw-600::text').re(r'^GSTIN No\.$').get()
        pan = response.css('span.mr-1.fw-600::text').re(r'^PAN No\.$').get()
        name = response.css('td.fw-600::text').re(r'^Name$').get()
        address = response.css('span.fw-600::text').re(r'^Permanent Address$').get()

        self.logger.info(f'GSTIN: {gstin}, PAN: {pan}, Name: {name}, Address: {address}')

        yield {
            'GSTIN No': gstin,
            'PAN No': pan,
            'Name': name,
            'Permanent Address': address
        }
