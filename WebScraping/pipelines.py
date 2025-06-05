# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

import re

class ProcessingCountry:

    fields_data = ['country-name','area','population','real-gdp-per-capita',
                   'unemployment-rate','taxes-and-other-revenues','debt-external',
                   'exchange-rates','internet-percent','internet-users','airports',
                   'merchant-marine','military-expenditures']
    fields_country = {field_data:re.sub(r'-','_',field_data) for field_data in fields_data}
    def process_item(self, item, spider):
        for field_country in self.fields_country.values():
                eval(f"self.clean__{field_country}(item)")

        return item
    
    """
    Functions for processing, extracted or clean 
    target values from a certain field
    """

    def clean__country_name(self,item) -> None:
        _field = 'country_name'

        _name = item[_field][1].strip()
        if _name != 'none':
            item[_field] = _name # Use short convention form
        else:
            item[_field] = item[_field][0].strip() # Otherwise use long convention form

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

    def clean__real_gdp_per_capita(self,item) -> None:
        _field = 'real_gdp_per_capita'
        item[_field] = self.__ExtractNumericValue(item,_field,int)

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

        # Deal when the US dollar is the national currency
        if 'US dollar is used' in item[_field][0]: 
            _exchange_rates = 1 # Use US dollar implies that has a exchange rate equal to 1
        else:
            _exchange_rates = self.__ExtractNumericValue(item,_field,float,1)

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
    def file_path(self,request,response=None,info=None,*,item=None):
        if item['country_name'][1]:
            _name = item['country_name'][1]
        else:
            _name = item['country_name'][0]
        return f'{_name.strip().lower()}.jpg'