import scrapy
from WebScraping.items import CountryItem

from .LinksCountries import GetLinksCountries

class CountrySpider(scrapy.Spider):
    name = 'CountryInformation'

    start_urls = GetLinksCountries()

    def parse(self,response):
        pass