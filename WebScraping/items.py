# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CountryItem(scrapy.Item):
    """
    Item container for scraped data from 
    information of a country in 
    https://www.cia.gov/the-world-factbook/
    """
    # Field for debugging
    country_url = scrapy.Field()

    # Fields for extracted data
    country_name = scrapy.Field() # Short country name
    area = scrapy.Field()
    population = scrapy.Field()
    real_gdp_purchasing_power_parity = scrapy.Field()
    unemployment_rate = scrapy.Field()
    taxes_and_other_revenues = scrapy.Field()
    debt_external = scrapy.Field()
    exchange_rates = scrapy.Field()
    internet_users = scrapy.Field() # Derived feature
    internet_percent = scrapy.Field()
    airports = scrapy.Field()
    merchant_marine = scrapy.Field()
    military_expenditures = scrapy.Field()
    
    # Field for extracted flag images
    image_urls = scrapy.Field()
    images = scrapy.Field() # Description and notes of country's flag
    image_name = scrapy.Field() # Name country's flag
    image_dump = scrapy.Field() # Populate by Scrapy