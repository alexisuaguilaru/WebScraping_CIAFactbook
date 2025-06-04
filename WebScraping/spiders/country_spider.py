import scrapy
from WebScraping.items import CountryItem
from playwright.async_api import async_playwright
from scrapy_playwright.page import PageMethod

import time
from .LinksCountries import GetLinksCountries

class CountrySpider(scrapy.Spider):
    name = 'CountryInformation'

    start_urls = ['https://www.cia.gov/the-world-factbook/countries/russia/'] # For testing
    # start_urls = GetLinksCountries()

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.parse_3,
                                 meta={'playwright': True,
                                       'playwright_include_page': True,
                                       'playwright_page_methods': [PageMethod('wait_for_timeout',2*1000)]},
                                 )
        
    def parse_3(self,response):
        country_data = CountryItem()
        return {'data' : response.xpath('//a[@href="/the-world-factbook/field/real-gdp-purchasing-power-parity/"]/../following-sibling::p').get()}