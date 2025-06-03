import re
import requests

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

    response_countries = requests.get(COUNTRY_LIST).json()['data']['countries']['nodes']
    for country_name in response_countries:
        yield BASE_URL.format(GetValidCountryName(country_name['name']))

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
    PatterCleanName = r"[\(\),']"
    clean_name = re.sub(PatterCleanName,'',CountryName)
    words_contry = map(str.lower,clean_name.split())
    return '-'.join(words_contry)