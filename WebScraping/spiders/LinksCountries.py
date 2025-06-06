import re
import requests
from time import sleep
from random import sample # For random testing

from typing import Iterator

def GetLinksCountries() -> Iterator[str]:
    """
    Function for getting links of each 
    country where its data belongs

    Returns
    -------
    country_link : str
        Yield a country link
    """
    BASE_URL = 'https://www.cia.gov/the-world-factbook/countries/{}/'
    COUNTRY_LIST = 'https://www.cia.gov/the-world-factbook/page-data/sq/d/5657653.json'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    response_countries = requests.get(COUNTRY_LIST,headers={'User-Agent':user_agent}).json()['data']['countries']['nodes']
    for country_name in response_countries:
        _name = GetValidCountryName(country_name['name'])
        yield BASE_URL.format(_name)

def GetValidCountryName(CountryName:str) -> str:
    """
    Function for getting the valid and 
    clean country name

    Parameters
    ----------
    CountryName : str
        Country's name

    Returns
    -------
    clean_country_name : str
        Clean and valid country's name
    """
    PatternCleanName = r"[\(\),']"
    clean_name = re.sub(PatternCleanName,'',CountryName)
    words_country = map(str.lower,clean_name.split())
    return '-'.join(words_country)

if __name__ == '__main__':
    print(*list(GetLinksCountries()),sep='\n')