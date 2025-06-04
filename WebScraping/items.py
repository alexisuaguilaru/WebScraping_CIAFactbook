# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
import scrapy

class CountryItem(scrapy.Item):
    """
    Item container for scraped data from 
    information of a country
    """
    # Fields for extracted data
    name_country = scrapy.Field()
    area = scrapy.Field()
    population = scrapy.Field()
    real_gdp = scrapy.Field()
    unemployment_rate = scrapy.Field()
    taxes = scrapy.Field()
    debt_external = scrapy.Field()
    exchange_rates = scrapy.Field()
    internet_users = scrapy.Field()
    internet_percent = scrapy.Field()
    airports = scrapy.Field()
    merchant_marine = scrapy.Field()
    militar_expenditures = scrapy.Field()
    
    # Field for extracted flag images
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_name = scrapy.Field()