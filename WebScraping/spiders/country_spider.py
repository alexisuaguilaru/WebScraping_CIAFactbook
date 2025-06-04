import scrapy
from WebScraping.items import CountryItem
from scrapy_playwright.page import PageMethod

import re

from .LinksCountries import GetLinksCountries

class CountrySpider(scrapy.Spider):
    name = 'CountryInformation'

    # For testing
    start_urls = ['https://www.cia.gov/the-world-factbook/countries/russia/',
                  'https://www.cia.gov/the-world-factbook/countries/bolivia/',
                  'https://www.cia.gov/the-world-factbook/countries/canada/',
                  'https://www.cia.gov/the-world-factbook/countries/greece/',
                  'https://www.cia.gov/the-world-factbook/countries/united-states-pacific-island-wildlife-refuges/'] 
    # start_urls = GetLinksCountries()

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.parse_data,
                                 meta={'playwright': True,
                                       'playwright_include_page': True,
                                       'playwright_page_methods': [PageMethod('wait_for_timeout',2*1000)]},
                                 )
    
    fields_data = ['country-name','area','population','real-gdp-per-capita',
                   'unemployment-rate','taxes-and-other-revenues','debt-external',
                   'exchange-rates','internet-users','airports',
                   'merchant-marine','military-expenditures']
    fields_country = {field_data:re.sub(r'-','_',field_data) for field_data in fields_data}
    fields_country['internet_users'] = 'internet_percent'
    element_data = '//a[@href="/the-world-factbook/field/{}/"]/../following-sibling::p'
    async def parse_data(self,response):
        country_data = CountryItem()
        for field_data in self.fields_data:
            country_data[self.fields_country[field_data]] = response.xpath(self.element_data.format(field_data)).get()

        yield country_data
        page = response.meta['playwright_page']
        await page.close()