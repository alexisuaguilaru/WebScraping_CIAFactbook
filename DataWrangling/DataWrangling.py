import marimo

__generated_with = "0.13.15"
app = marimo.App()


@app.cell
def _():
    # 0. Import Libraries
    return


@app.cell
def _():
    # Essential libraries for Marimo

    import marimo as mo
    return (mo,)


@app.cell
def _():
    # Import Libraries

    import pandas as pd
    import numpy as np

    import seaborn as sns
    import matplotlib.pyplot as plt
    return (pd,)


@app.cell
def _():
    # Other code 

    import SourceDataWrangling as src

    PATH_DATASET = './Dataset/'
    RANDOM_STATE = 8013
    return PATH_DATASET, RANDOM_STATE, src


@app.cell
def _(mo):
    mo.md(r"# 1. Load Dataset")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        First the data set obtained from the Web Scraping process is loaded, in order to determine missing or null values in the different attributes.
    
        Based on [Requirements](../RequirementsDocument.pdf), the attributes are renamed to match those specified and those relevant to the study are retained.
    
        By performing the Web Scraping was acquired the knowledge to determine why several of the attributes have null values. In all cases it is related to the fact that the field is empty or its value is `0` or some other specific value.
        """
    )
    return


@app.cell
def _(PATH_DATASET, pd):
    WorldFactbook_Dataset_Raw = pd.read_csv(PATH_DATASET+'Dataset_Raw.csv')

    _features_renaming = {
        'country_name' : 'name',
        'real_gdp_per_capita' : 'gdp',
        'unemployment_rate' : 'unemployment',
        'taxes_and_other_revenues' : 'taxes',
        'debt_external' : 'debt',
    }

    Features = [
        'name',
        'area',
        'population',
        'gdp',
        'unemployment',
        'taxes',
        'debt',
        'exchange_rates',
        'internet_users',
        'internet_percent',
        'airports',
        'merchant_marine',
        'military_expenditures',
        'image_urls',
    ]

    WorldFactbook_Dataset_Raw_1 = WorldFactbook_Dataset_Raw.rename(columns=_features_renaming)[Features]
    return (WorldFactbook_Dataset_Raw_1,)


@app.cell
def _(RANDOM_STATE, WorldFactbook_Dataset_Raw_1, mo):
    _sample_countries = WorldFactbook_Dataset_Raw_1.sample(5,random_state=RANDOM_STATE)
    mo.vstack(
        [
            mo.md('##Examples of Countries'),
            _sample_countries,
        ]
    )
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_1, mo):
    _null_values_feature = WorldFactbook_Dataset_Raw_1.isnull().sum()
    mo.vstack(
        [
            mo.md('##Count of Null Values by Feature'),
            _null_values_feature,
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"As shown, many of the attributes have missing values, which can be explained by using the knowledge acquired during Web Scraping. And as explained below some of these values can be properly imputed.")
    return


@app.cell
def _(mo):
    mo.md(r"# 2. Data Wrangling")
    return


@app.cell
def _(mo):
    mo.md(r"For each feature with missing or null values, it is determined, by means of what that feature represents, which value will be useb to fill the missing values.")
    return


@app.cell
def _(mo):
    mo.md(r"## 2.1 Drop `'World'` Entry")
    return


@app.cell
def _(mo):
    mo.md(r"During Web Scraping, it was detected that global data (World) was extracted, so it will first be eliminated because it is not of interest for the study.")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_1):
    # Keeping all the countries except 'World'

    WorldFactbook_Dataset_Raw_2 = WorldFactbook_Dataset_Raw_1.query("name != 'World'")

    WorldFactbook_Dataset_Raw_2.reset_index(drop=True,inplace=True)
    return (WorldFactbook_Dataset_Raw_2,)


@app.cell
def _(mo):
    mo.md(r"## 2.2 `population` Feature")
    return


@app.cell
def _(mo):
    mo.md(r"Of the countries or entries that do not have `population` values, in most cases they are uninhabited islands or places with temporary inhabitants. Therefore, in both cases there are no inhabitants (population is zero).")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Exploring countries without `population`

    WorldFactbook_Dataset_Raw_2.query("population != population")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2, src):
    # Filling missing values on `population` with 0

    WorldFactbook_Dataset_Raw_2__population = src.FillMissingValues(WorldFactbook_Dataset_Raw_2,'population',0)
    return


@app.cell
def _(mo):
    mo.md(r"## 2.3 `gdp` Feature")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Due to the importance that this feature represents for the study, it is necessary to be careful about the value assigned for imputation, but as many of the missing values are for islands, protected areas and oceans, the best value is `0`.
    
        In addition to all this, it should be considered that these islands or territories are incorporated to a country, so the value of its `GDP` could be equal to that of the country to which it belongs.
        """
    )
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Exploring countries without `gdp`

    WorldFactbook_Dataset_Raw_2.query("gdp != gdp")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2, src):
    # Filling missing values on `gdp` with 0

    WorldFactbook_Dataset_Raw_2__gdp = src.FillMissingValues(WorldFactbook_Dataset_Raw_2,'gdp',0)
    return


@app.cell
def _(mo):
    mo.md(r"## 2.4 `unemployment` Feature")
    return


@app.cell
def _(mo):
    mo.md(r"In several of the missing data are from non-productive islands or there is not enough data to determine the unemployment rate; therefore, under these considerations, the missing values can be imputed with `0`, although the mean could be used to indicate that they behave as the average unemployment rate of the countries.")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Exploring countries without `unemployment`

    WorldFactbook_Dataset_Raw_2.query("unemployment != unemployment")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2, src):
    # Filling missing values on `unemployment` with 0

    WorldFactbook_Dataset_Raw_2__unemployment = src.FillMissingValues(WorldFactbook_Dataset_Raw_2,'unemployment',0)
    return


@app.cell
def _(mo):
    mo.md(r"## 2.5 `taxes` Feature")
    return


@app.cell
def _(mo):
    mo.md(r"Although many of the missing values belong to islands, taxes still apply, so these missing values in `taxes` should be imputed with the average of all countries. This is done to represent that they have a behavior similar to the global average.")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Exploring countries without `taxes`

    WorldFactbook_Dataset_Raw_2.query("taxes != taxes")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2, src):
    # Filling missing values on `taxes` with its mean

    _mean_taxes = WorldFactbook_Dataset_Raw_2['taxes'].mean()
    WorldFactbook_Dataset_Raw_2__taxes = src.FillMissingValues(WorldFactbook_Dataset_Raw_2,'taxes',_mean_taxes)
    return


@app.cell
def _(mo):
    mo.md(r"## 2.6 `debt` Feature")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Since there are many missing values in this feature, in addition to the fact that not all countries are islands or natural areas, this imputation becomes delicate.
    
        A candidate value for this imputation is to use the median of `debt`, because the median allows to indicate that these countries with missing values will have a behavior similar to `50%` of the countries with `debt`, that is, it is assumed that their debt is at most the median of `debt`.
        """
    )
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Exploring countries without `debt`

    WorldFactbook_Dataset_Raw_2.query("debt != debt")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2, src):
    # Filling missing values on `debt` with its mean

    _median_debt = WorldFactbook_Dataset_Raw_2['debt'].median()
    WorldFactbook_Dataset_Raw_2__debt = src.FillMissingValues(WorldFactbook_Dataset_Raw_2,'debt',_median_debt)
    return


@app.cell
def _(mo):
    mo.md(r"## 2.7 `exchange_rates` Feature")
    return


@app.cell
def _(mo):
    mo.md(r"In the countries that do not have this feature, two cases are detected: either they are islands belonging to a country or they do not have a national currency. Therefore, a manual imputation is performed for the missing values with the values of the corresponding countries and in the case that they do not have a national currency, it is left as `1`.")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Exploring countries without `exchange_rates`

    WorldFactbook_Dataset_Raw_2.query("exchange_rates != exchange_rates")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Manual filling missing values on `exchange_rates`

    _index_missing__exchange_rates = WorldFactbook_Dataset_Raw_2.query("exchange_rates != exchange_rates").index
    _filling_values__exchange_rates = [1,1.515,
                                       10.746,0.924,
                                       1.515,0.924,
                                       1.515,10.746,
                                       1.369,1,
                                       1,0.782,
                                       1.369,1.369]

    WorldFactbook_Dataset_Raw_2__exchange_rates = WorldFactbook_Dataset_Raw_2['exchange_rates'].copy()
    WorldFactbook_Dataset_Raw_2__exchange_rates.iloc[_index_missing__exchange_rates] = _filling_values__exchange_rates
    return


@app.cell
def _(mo):
    mo.md(r"## 2.8 `internet_users` Feature")
    return


@app.cell
def _(mo):
    mo.md(r"In most cases these are uninhabited islands, protected areas or public information, so the `internet_users` feature does not have a value, i.e. it is `0`.")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Exploring countries without `internet_users`

    WorldFactbook_Dataset_Raw_2.query("internet_users != internet_users")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2, src):
    # Filling missing values on `internet_users` with 0

    WorldFactbook_Dataset_Raw_2__internet_users = src.FillMissingValues(WorldFactbook_Dataset_Raw_2,'internet_users',0)
    return


@app.cell
def _(mo):
    mo.md(r"## 2.9 `internet_percent` Feature")
    return


@app.cell
def _(mo):
    mo.md(r"As in `internet_users`, missing values in `internet_percent` are imputed with `0`.")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Exploring countries without `internet_percent`

    WorldFactbook_Dataset_Raw_2.query("internet_percent != internet_percent")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2, src):
    # Filling missing values on `internet_percent` with 0

    WorldFactbook_Dataset_Raw_2__internet_percent = src.FillMissingValues(WorldFactbook_Dataset_Raw_2,'internet_percent',0)
    return


@app.cell
def _(mo):
    mo.md(r"## 2.10 `airports` Feature")
    return


@app.cell
def _(mo):
    mo.md(r"Of the countries with missing values in `airports`, most are uninhabited islands or countries that have access to this infrastructure using other means. Therefore, missing values are imputed with `0`.")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Exploring countries without `airports`

    WorldFactbook_Dataset_Raw_2.query("airports != airports")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2, src):
    # Filling missing values on `airports` with 0

    WorldFactbook_Dataset_Raw_2__airports = src.FillMissingValues(WorldFactbook_Dataset_Raw_2,'airports',0)
    return


@app.cell
def _(mo):
    mo.md(r"## 2.11 `merchant_marine` Feature")
    return


@app.cell
def _(mo):
    mo.md(r"The fact that they do not have the `merchant_marine` attribute can be related to the fact that they are landlocked countries or regions, countries that do not have port infrastructure or are uninhabited islands. Therefore, in these three cases, `merchant_marine` is imputed with `0`.")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Exploring countries without `merchant_marine`

    WorldFactbook_Dataset_Raw_2.query("merchant_marine != merchant_marine")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2, src):
    # Filling missing values on `merchant_marine` with 0

    WorldFactbook_Dataset_Raw_2__merchant_marine = src.FillMissingValues(WorldFactbook_Dataset_Raw_2,'merchant_marine',0)
    return


@app.cell
def _(mo):
    mo.md(r"## 2.12 `military_expenditures` Feature")
    return


@app.cell
def _(mo):
    mo.md(r"Countries that do not have `military_expenditures` verify that they are islands, are not publicly available their data or do not have military expenditures. Although some of the countries do have military expenditures (although they are not publicly reported), the best strategy is to impute the missing values with the global average of `military_expenditures`; this is to indicate that they have a similar trend to the global behavior.")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Exploring countries without `military_expenditures`

    WorldFactbook_Dataset_Raw_2.query("military_expenditures != military_expenditures")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2, src):
    # Filling missing values on `military_expenditures` with its mean

    _median_military_expenditures = WorldFactbook_Dataset_Raw_2['military_expenditures'].median()
    WorldFactbook_Dataset_Raw_2__military_expenditures = src.FillMissingValues(WorldFactbook_Dataset_Raw_2,'military_expenditures',_median_military_expenditures)
    return


@app.cell
def _(mo):
    mo.md(r"## 2.13 `image_urls` Feature")
    return


@app.cell
def _(mo):
    mo.md(r"Of the countries that do not have the image of their flag, it is because the page [CIA: The World Factbook](https://www.cia.gov/the-world-factbook/) does not have the representative flag of those countries.")
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Exploring countries without `image_urls`

    WorldFactbook_Dataset_Raw_2.query("image_urls != image_urls")
    return


@app.cell
def _(mo):
    mo.md(r"# 3. Dump Modified Dataset")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Once the missing values have been processed, manual adjustments are made on `name` for some special cases on the names. Afterwards, Data Wrangling is applied to the final data set.
    
        Finally, the `gdp` values are encoded in categorical values following the conventions established in [Requirements](../RequirementsDocument.pdf).
    
        And with this last modification, the dataset is saved with the last modifications.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"## 3.1 Renaming Country Names")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The names of the following entries are renamed using the consequent names:
    
        * Svalbard (sometimes referred to as Spitsbergen, the largest island in the archipelago) $\to$ Svalbard
    
        * Baker Island, Howland Island, Jarvis Island, Johnston Atoll, Kingman Reef, Midway Islands, Palmyra Atoll $\to$ United States Pacific Island Wildlife Refuges
        """
    )
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2):
    # Renaming some values in `name`

    WorldFactbook_Dataset_Raw_3 = WorldFactbook_Dataset_Raw_2.copy()

    _index_long_names = [217,240]
    _rename_long_names = ['Svalbard','United States Pacific Island Wildlife Refuges']

    WorldFactbook_Dataset_Raw_3.loc[_index_long_names,'name'] = _rename_long_names
    return (WorldFactbook_Dataset_Raw_3,)


@app.cell
def _(mo):
    mo.md(r"## 3.2 Merge Individual Data Wrangling")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        From the different considerations and imputation values to perform the [Data Wrangling](#2-data-wrangling), they are applied to the final dataset, and it is checked that it has no missing values except in `image_urls`.
    
        As the last point is verified, the Data Wrangling has been properly performed on the dataset.
        """
    )
    return


@app.cell
def _(WorldFactbook_Dataset_Raw_2, WorldFactbook_Dataset_Raw_3):
    # Applying Data Wrangling 

    WorldFactbook_Dataset_Raw_3_Wrangling = WorldFactbook_Dataset_Raw_3.copy()

    for _feature in WorldFactbook_Dataset_Raw_2.columns:
        try:
            _data_wrangling_feature = eval(f'WorldFactbook_Dataset_Raw_2__{_feature}')
            WorldFactbook_Dataset_Raw_3_Wrangling[_feature] = _data_wrangling_feature
        except:
            continue
    return (WorldFactbook_Dataset_Raw_3_Wrangling,)


@app.cell
def _(WorldFactbook_Dataset_Raw_3_Wrangling, mo):
    mo.vstack(
        [
            mo.md('**Count of Null Values by Feature**'),
            WorldFactbook_Dataset_Raw_3_Wrangling.isnull().sum(),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"## 3.3 Encode `gdp` Feature")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Following the conventions and notation in [Requirements](../RequirementsDocument.pdf), the `gdp_encode` feature is generated based on `gdp` with the following rules:
    
        * `low-income` $\implies$ `gdp` $\le 1.0$ billions
    
        * `average-income` $\implies 1.0 <$ `gdp` $\le 3.0$ billions
    
        * `high-income` $\implies$ `gdp` $3.0 >$ billions
        """
    )
    return


@app.cell
def _(RANDOM_STATE, WorldFactbook_Dataset_Raw_3_Wrangling, mo, src):
    # Encoding `gdp`

    WorldFactbook_Dataset = WorldFactbook_Dataset_Raw_3_Wrangling.copy()

    WorldFactbook_Dataset['gdp_encode'] = src.EncoderGDP(WorldFactbook_Dataset)


    _sample_countries = WorldFactbook_Dataset.sample(5,random_state=RANDOM_STATE)
    mo.vstack(
        [
            mo.md('**Examples of Processed Countries**'),
            _sample_countries,
        ]
    )
    return (WorldFactbook_Dataset,)


@app.cell
def _(mo):
    mo.md(r"## 3.4 Dump Dataset")
    return


@app.cell
def _(mo):
    mo.md(r"With the last modifications made, it proceeds with saving the data set without missing values and with the pertinent modifications.")
    return


@app.cell
def _(PATH_DATASET, WorldFactbook_Dataset):
    # Dumping dataset 

    WorldFactbook_Dataset.to_csv(PATH_DATASET+'Dataset.csv')
    return


if __name__ == "__main__":
    app.run()
