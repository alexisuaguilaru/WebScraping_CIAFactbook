import marimo

__generated_with = "0.13.15"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"<img src='https://raw.githubusercontent.com/alexisuaguilaru/WebScraping_CIAFactbook/refs/heads/main/Resources/Proyecto03_EDA_AlexisAguilar.png' alt='cover'>")
    return


@app.cell
def _(mo):
    mo.md(r"# Introduction")
    return


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
    return np, pd, sns


@app.cell
def _():
    # Other code 

    import SourceExploratoryDataAnalysis as src

    PATH_DATASET = './Dataset/'
    RANDOM_STATE = 8013
    return PATH_DATASET, RANDOM_STATE


@app.cell
def _(mo):
    mo.md(r"# 1. Load Dataset")
    return


@app.cell
def _(PATH_DATASET, RANDOM_STATE, pd):
    WorldFactbook_Dataset = pd.read_csv(PATH_DATASET+'Dataset.csv')

    WorldFactbook_Dataset.sample(5,random_state=RANDOM_STATE)
    return (WorldFactbook_Dataset,)


@app.cell
def _(mo):
    mo.md(r"# 2. Data Clean")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Because several of the data related to islands are not relevant to the study, they are to be discarded; these islands are satisfied that either of their two values in `gdp` or `internet_users` are `0`.
    
        Therefore, the main data cleaning becomes the elimination of these data that do not contribute much to the discussion about the relationship of these two attributes.
        """
    )
    return


@app.cell
def _():
    # Defining useful variables

    gdp = 'gdp'
    internet_users = 'internet_users'
    gdp_encode = 'gdp_encode'
    return gdp, gdp_encode, internet_users


@app.cell
def _(WorldFactbook_Dataset, gdp, internet_users):
    # Dropping countries with `0` values in `gdp` or `internet_users`

    WorldFactbook_Dataset_Clean = WorldFactbook_Dataset.query(f"0 < {gdp} & 0 < {internet_users}")
    return (WorldFactbook_Dataset_Clean,)


@app.cell
def _(mo):
    mo.md(r"# 3. Relationship Between `gdp` and `internet_users`")
    return


@app.cell
def _(WorldFactbook_Dataset_Clean, gdp, np, sns):
    _data_x = np.log10(WorldFactbook_Dataset_Clean[gdp])
    sns.histplot(WorldFactbook_Dataset_Clean,x=_data_x)
    return


@app.cell
def _(WorldFactbook_Dataset_Clean, internet_users, np, sns):
    _data_x = np.log10(WorldFactbook_Dataset_Clean[internet_users])
    sns.histplot(WorldFactbook_Dataset_Clean,x=_data_x)
    return


@app.cell
def _(WorldFactbook_Dataset_Clean, gdp, gdp_encode, internet_users, np, sns):
    _data_x = np.log10(WorldFactbook_Dataset_Clean[gdp])
    _data_y = np.log10(WorldFactbook_Dataset_Clean[internet_users])

    sns.scatterplot(x=_data_x,y=_data_y,hue=WorldFactbook_Dataset_Clean[gdp_encode])
    return


@app.cell
def _(mo):
    mo.md(r"# Conclusions")
    return


if __name__ == "__main__":
    app.run()
