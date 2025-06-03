# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
import scrapy

@dataclass
class CountryItem(scrapy.Item):
    """
    Item container for scraped data from 
    information of a country
    """
    # Fields for extracted data
    name_country : str
    area : int
    population : int
    real_gdp : int
    unemployment_rate : float
    taxes : float
    debt_external : int
    exchange_rates : float
    internet_users : int
    internet_percent : float
    airports : int
    merchant_marine : int
    militar_expenditures : float
    
    # Field for extracted flag images
    image_urls : str
    images : str
    image_name : str