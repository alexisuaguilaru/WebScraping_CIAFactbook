# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from scrapy.pipelines.images import ImagesPipeline

import logging
import re

class ProcessingCountry:
    """
    Pipeline for cleaning each data field of 
    a CountryItem
    """

    # Data field being extracted for a country
    fields_data = ['country-name','area','population','real-gdp-purchasing-power-parity',
                   'unemployment-rate','taxes-and-other-revenues','debt-external',
                   'exchange-rates','internet-percent','internet-users','airports',
                   'merchant-marine','military-expenditures','images']
    fields_country = {field_data:re.sub(r'-','_',field_data) for field_data in fields_data}
    def process_item(self, item, spider):
        """
        Method for cleaning each data field of a 
        CountryItem and get its value
        """
        for field_country in self.fields_country.values():
            try:
                eval(f"self.clean__{field_country}(item)")
            except:
                logging.info(f'[FIELD ERROR {field_country}] {item["country_url"]}')

        return item
    
    """
    Functions for processing, extracted or clean 
    target values from a certain field
    """

    def clean__country_name(self,item) -> None:
        _field = 'country_name'

        if item[_field]:
            _name = item[_field][1].strip()
            if _name == 'none': # Use short convention form if exists
                _name = item[_field][0].strip() # Otherwise use long convention form
        else: # Whether 'country_name' does not exist, use name from URL
            _name = item['country_url'].split('/')[-2]
            _name = _name.split('-')
            _name = ' '.join(map(str.capitalize,_name))

        item[_field] = _name

    def clean__area(self,item) -> None:
        _field = 'area'
        _area = self.__ExtractNumericValue(item,_field,float)

        # Deal with millions of sq km
        if 'million' in item[_field][0]:
            _area *= 10**6

        item[_field] = _area

    def clean__population(self,item) -> None:
        _field = 'population'
        item[_field] = self.__ExtractNumericValue(item,_field,int)

    def clean__real_gdp_purchasing_power_parity(self,item) -> None:
        _field = 'real_gdp_purchasing_power_parity'
        _real_gdp_per_capita = self.__ExtractNumericValue(item,_field,float)
        if 'million' in item[_field][0]:
            _real_gdp_per_capita *= 10**6
        elif 'billion' in item[_field][0]:
            _real_gdp_per_capita *= 10**9
        elif 'trillion' in item[_field][0]:
            _real_gdp_per_capita *= 10**12
    
        item[_field] = _real_gdp_per_capita

    def clean__unemployment_rate(self,item) -> None:
        _field = 'unemployment_rate'
        item[_field] = self.__ExtractNumericValue(item,_field,float)

    def clean__taxes_and_other_revenues(self,item) -> None:
        _field = 'taxes_and_other_revenues'
        item[_field] = self.__ExtractNumericValue(item,_field,float)

    def clean__debt_external(self,item) -> None:
        _field = 'debt_external'
        _debt_external = self.__ExtractNumericValue(item,_field,float)

        # Deal with scaling factor of debt
        if _debt_external:
            if 'million' in item[_field][0]:
                _debt_external *= 10**6
            elif 'billion' in item[_field][0]:
                _debt_external *= 10**9

        item[_field] = _debt_external

    def clean__exchange_rates(self,item) -> None:
        _field = 'exchange_rates'

        if item[_field]:
            # Deal when the US dollar is the national currency
            if 'US dollar is used' in item[_field][0] or 'US dollar became' in item[_field][0]: 
                _exchange_rates = 1 # Use US dollar implies that has a exchange rate equal to 1
            elif 'entry for the West Bank' in item[_field][0]: # Data entry manual, special case for Gaza Strip
                 _exchange_rates = 3.36
            else:
                _exchange_rates = self.__ExtractNumericValue(item,_field,float,1)
        else:
            _exchange_rates = None

        item[_field] = _exchange_rates

    def clean__internet_percent(self,item) -> None:
        _field = 'internet_percent'
        item[_field] = self.__ExtractNumericValue(item,_field,float)

    def clean__internet_users(self,item) -> None:
        _field = 'internet_users'

        # It is derived feature because is not found in the page
        if (_internet_percent:=item['internet_percent']) and (_population:=item['population']):
            _internet_users = round(_population*_internet_percent)
        else:
            _internet_users = None

        item[_field] = _internet_users

    def clean__airports(self,item) -> None:
        _field = 'airports'
        item[_field] = self.__ExtractNumericValue(item,_field,int)

    def clean__merchant_marine(self,item) -> None:
        _field = 'merchant_marine'
        item[_field] = self.__ExtractNumericValue(item,_field,int)

    def clean__military_expenditures(self,item) -> None:
        _field = 'military_expenditures'
        item[_field] = self.__ExtractNumericValue(item,_field,float)

    def clean__images(self,item) -> None:
        _field = 'images'
        # Deal with descriptions and notes for country flags
        item[_field] = ''.join(item[_field])

    """
    Auxiliar functions for getting certain values and other routines
    """

    def __ExtractNumericValue(self,item,field:str,dtype,index:int=0) -> int | float | None:
        if dtype == int:
            get_numeric_value = self.__GetIntegerValue
        elif dtype == float:
            get_numeric_value = self.__GetFloatValue

        if item[field]:
            _extracted_value = get_numeric_value(item,field,index)
            if _extracted_value:
                _extracted_value = _extracted_value.group()
                _extracted_value = self.__CleanNumericValue(_extracted_value)
                _extracted_value = dtype(_extracted_value)
            else: # If there is a weird value no-numeric
                _extracted_value = None
        else: # If field not found or without registries
            _extracted_value = None

        return _extracted_value

    def __GetIntegerValue(self,item,field:str,index:int=0) -> re.Match | None:
        return re.search(r'[0-9][0-9,]*',item[field][index])

    def __GetFloatValue(self,item,field:str,index:int=0) -> re.Match | None:
        return re.search(r'[0-9][0-9,\.]*',item[field][index])
    
    def __CleanNumericValue(self,value:str) -> str:
        return re.sub(r',','',value)


class ImagesCountry(ImagesPipeline):
    """
    Pipeline for downloading the flag image 
    of a country 
    """
    def file_path(self,request,response=None,info=None,*,item=None):
        """
        Custom method for defining the file name for 
        the download flag country image
        """
        logging.info(f'[FLAG BEING DONWLOADED] {item["country_url"]}')

        _image_name = item['country_name']
        _image_name = re.sub(r"[\(\),']",'',_image_name)
        _image_name = '-'.join(_image_name.lower().split())

        _image_name = f'{_image_name}.jpg'
        item['image_name'] = _image_name
        return _image_name