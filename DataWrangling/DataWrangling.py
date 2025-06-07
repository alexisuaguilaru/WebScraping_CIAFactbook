import marimo

__generated_with = "0.13.15"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"# 0. Import LIbraries")
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
    mo.md(r"# 1. Load Dataset and First Exploration")
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
    WorldFactbook_Dataset_Raw_2 = WorldFactbook_Dataset_Raw_1.query("name != 'World'")
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
def _(WorldFactbook_Dataset_Raw_2, src):
    WorldFactbook_Dataset_Raw_2__population = src.FillMissingValues(WorldFactbook_Dataset_Raw_2,'population',0)
    return


if __name__ == "__main__":
    app.run()
