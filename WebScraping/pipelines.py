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
                   'exchange-rates','internet-users','airports',
                   'merchant-marine','military-expenditures']
    fields_country = {field_data:re.sub(r'-','_',field_data) for field_data in fields_data}
    fields_country['internet_users'] = 'internet_percent'
    def process_item(self, item, spider):
        # for field_country in self.fields_country.values():
                # eval(f"self.clean__{field_country}(item)")

        return item
    
    def clean__country_name(self,item):
        _name = item['country_name'][1].strip()
        if _name != 'none':
            item['country_name'] = _name # use short convention form
        else:
            item['country_name'] = item['country_name'][0].strip() # otherwise use long convention form

    def clean__area(self,item):
        _area = re.search(r'[0-9,\.]+',item['area'][0]).group()
        _area = re.sub(r',','',_area)

        # Deal with millions of sq km
        if '.' in _area:
            _area = float(_area)*(10**6)

        item['area'] = int(_area)
    
class ImagesCountry(ImagesPipeline):
    def file_path(self,request,response=None,info=None,*,item=None):
        if item['country_name'][1]:
            _name = item['country_name'][1]
        else:
            _name = item['country_name'][0]
        return f'{_name.strip().lower()}.jpg'