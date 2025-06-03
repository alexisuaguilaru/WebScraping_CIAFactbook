import scrapy

from .LinksCountries import GetLinksCountries

class CountrySpider(scrapy.Spider):
    name = 'CountryInformation'

    # start_urls = GetLinksCountries()
    start_urls = ['https://www.cia.gov/the-world-factbook/countries/']

    def parse(self,response):
        for country_link in response.xpath('//a[contains(@class,"inline-link")]/@href'):
            yield {'name':country_link}

