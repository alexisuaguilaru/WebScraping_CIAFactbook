import scrapy
from WebScraping.items import CountryItem
from scrapy_playwright.page import PageMethod

import logging
import re

from .LinksCountries import GetLinksCountries


class CountrySpider(scrapy.Spider):
    """
    Main spider for web scraping of data 
    and information of a country in 
    https://www.cia.gov/the-world-factbook/ 
    """

    name = 'CountryInformation'
    meta_playwright = {'playwright': True,
                       'playwright_include_page': True,
                       'playwright_page_methods': [PageMethod('wait_for_timeout',4*1000)]}

    # For testing
    start_urls = [
                  'https://www.cia.gov/the-world-factbook/countries/gaza-strip/',
                 ] 
    
    # For deployment
    # start_urls = GetLinksCountries()

    async def start(self):
        for counter_urls , url in enumerate(self.start_urls,1):
            yield scrapy.Request(url,callback=self.parse_data,meta=self.meta_playwright)
    
    # Data field being extracted for a country
    fields_data = ['country-name','area','population','real-gdp-per-capita',
                   'unemployment-rate','taxes-and-other-revenues','debt-external',
                   'exchange-rates','internet-users','airports',
                   'merchant-marine','military-expenditures']
    fields_country = {field_data:re.sub(r'-','_',field_data) for field_data in fields_data}
    fields_country['internet-users'] = 'internet_percent'
    # Using 'Web Inspection' and Scrapy Shell, each field is relative to a anchor with a href specific to a field
    element_data = '//a[@href="/the-world-factbook/field/{}/"]/../following-sibling::p/text()'
    async def parse_data(self,response):
        """
        Method for getting each data field being extracted 
        from https://www.cia.gov/the-world-factbook/ without 
        process (transform) it of a country
        """
        logging.info(f'[COUNTRY BEING EXTRACTED] {response.url}')
        
        country_data = CountryItem()

        for field_data in self.fields_data:
            country_data[self.fields_country[field_data]] = response.xpath(self.element_data.format(field_data)).getall()
        
        country_data['country_url'] = response.url

        if response.xpath('//div[@class="card-gallery__text-container"]/div/span/text()').get() == 'Country Flag': # Whether there is an actual flag image to donwload
            # Request for adding image relative data to a CountryItem
            yield scrapy.Request(response.url+'flag/',callback=self.parse_image,meta={**self.meta_playwright,'country-data':country_data})
        else:
            logging.info(f'[COUNTRY WITHOUT FLAG IMAGE] {response.url}')
            country_data['image_urls'] = []
            country_data['images'] = ''
            country_data['image_name'] = '404.jpg'
            yield country_data

        page = response.meta['playwright_page']
        await page.close()

    async def parse_image(self,response):
        """
        Method for getting each image relative field being 
        extracted from https://www.cia.gov/the-world-factbook/ 
        of a country's flag
        """
        country_data = response.meta['country-data']

        image_uri = response.xpath('//img[starts-with(@src,"/the-world-factbook/static/")]/@src').get()
        country_data['image_urls'] = [response.urljoin(image_uri)]
        country_data['images'] = response.xpath('//div[contains(@class,"image-detail-block-caption")]/text()').getall()

        yield country_data

        page = response.meta['playwright_page']
        await page.close()