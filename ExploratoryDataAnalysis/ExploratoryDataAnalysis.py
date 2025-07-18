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
def _(mo):
    mo.md(
        r"""
        The following notebook aims to develop the facts and evidence to show whether there is a relationship between `gdp` and `internet_percent`, that is, the main questions of the study [[1]](#references). For this, a [Data Cleaning](#2-data-clean) is performed to discard some countries, mainly islands, which do not contribute much information to the discussion.
    
        Afterwards, a simple study of the variables to be used to reveal the salient facts and their impact in a more real context is carried out in [Univariate Analysis](#3-univariate-analysis-of-gdp-and-internet_users). And finally to test the relationship of the study by means of hypothesis tests based on the correlation of two variables are presented in [Relationship between `gdp` and `internet_percent`](#4-relationship-between-gdp-and-internet_percent) and [Relationship between `gdp` and `internet_percent by Type of Incomde](#5-relationship-between-gdp-and-internet_percent-by-type-of-income).
        """
    )
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
    from scipy import stats

    import seaborn as sns
    import matplotlib.pyplot as plt
    return np, pd, stats


@app.cell
def _():
    # Other code 

    import SourceExploratoryDataAnalysis as src

    PATH_DATASET = './Dataset/'
    RANDOM_STATE = 8013
    return PATH_DATASET, RANDOM_STATE, src


@app.cell
def _(mo):
    mo.md(r"# 1. Load Dataset")
    return


@app.cell
def _(mo):
    mo.md(r"The final dataset after applying the data wrangling operations is loaded for cleaning and analysis of your data of interest.")
    return


@app.cell
def _(PATH_DATASET, RANDOM_STATE, pd):
    WorldFactbook_Dataset = pd.read_csv(PATH_DATASET+'Dataset.csv')

    WorldFactbook_Dataset.sample(5,random_state=RANDOM_STATE)
    return (WorldFactbook_Dataset,)


@app.cell
def _(mo):
    mo.md(r"# 2. Data Cleaning")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Because several of the data related to islands are not relevant to the study, they are to be discarded; these islands are satisfied that either of their two values in `gdp` or `internet_percent` are `0`.
    
        Therefore, the main data cleaning becomes the elimination of these data that do not contribute much to the discussion about the relationship of these two attributes.
        """
    )
    return


@app.cell
def _():
    # Defining useful variables

    gdp = 'gdp'
    internet_percent = 'internet_percent'
    type_income = 'gdp_encode'
    return gdp, internet_percent, type_income


@app.cell
def _(WorldFactbook_Dataset, gdp, internet_percent):
    # Dropping countries with `0` values in `gdp` or `internet_users`

    WorldFactbook_Dataset_Clean = WorldFactbook_Dataset.query(f"0 < {gdp} & 0 < {internet_percent}")
    return (WorldFactbook_Dataset_Clean,)


@app.cell
def _(mo):
    mo.md(r"# 3. Univariate Analysis of `gdp` and `internet_users`")
    return


@app.cell
def _(mo):
    mo.md(r"## 3.1 Analysis of `gdp`")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        As expected, many of the countries will tend to have a low GDP, this is related to the distribution of global wealth; therefore, there are countries with very high incomes that could be considered, theoretically, outliers. To reduce this phenomenon, the `log10` function is applied, thus generating a distribution that tends to be normal instead of exponential.
    
        Using the Shapiro-Wilk test for normality of data, it is found that, by the p-value, the transformed data follow a normal distribution. This will allow to apply parametric tests on the correlation of two variables.
    
        Without transforming the data, the mean is equal to $0.8569$ trillions, showing that most of the countries have low incomes or are in a state of poverty. But there are very extreme cases, this when considering the standard deviation reported.
        """
    )
    return


@app.cell
def _(WorldFactbook_Dataset_Clean, gdp, mo, src):
    _plot = src.PlotUnivariateFeature(WorldFactbook_Dataset_Clean,gdp,False)
    _plot_log10 = src.PlotUnivariateFeature(WorldFactbook_Dataset_Clean,gdp)

    mo.vstack([_plot,_plot_log10])
    return


@app.cell
def _(WorldFactbook_Dataset_Clean, gdp, np, stats):
    _result = stats.shapiro(np.log10(WorldFactbook_Dataset_Clean[gdp]))

    print(f'P-value of Shapiro-Wilk Test: {_result.pvalue}')
    return


@app.cell
def _(WorldFactbook_Dataset_Clean, gdp, src):
    src.DescriptiveAnalysis(WorldFactbook_Dataset_Clean,gdp)
    return


@app.cell
def _(mo):
    mo.md(r"## 3.1 Analysis of `internet_percent`")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Noting that the distribution has a negative skew, it can be said that Internet accessibility has increased, in the sense that most countries will tend to have high Internet coverage among their population.
    
        The latter represents that the values are concentrated in a reduced range of values, implying that its variance tends to be low, although it has a high value ($25.54%) but this is due to the outliers or countries that do not have sufficient infrastructure for Internet access.
        """
    )
    return


@app.cell
def _(WorldFactbook_Dataset_Clean, internet_percent, src):
    _plot = src.PlotUnivariateFeature(WorldFactbook_Dataset_Clean,internet_percent,False)

    _plot
    return


@app.cell
def _(WorldFactbook_Dataset_Clean, internet_percent, src):
    src.DescriptiveAnalysis(WorldFactbook_Dataset_Clean,internet_percent)
    return


@app.cell
def _(mo):
    mo.md(r"# 4. Relationship Between `gdp` and `internet_percent`")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The Pearson Correlation Test is used to prove that the correlation is statistically significant in order to show that this relationship exists.
    
        By using the `gdp` values without transforming, it is proved that they have a statistically significant correlation. This implies that as a country's purchasing power increases so does Internet access and this makes sense because there is more investment in telecommunications infrastructure in both the public and private sectors.
        """
    )
    return


@app.cell
def _(WorldFactbook_Dataset_Clean, gdp, internet_percent, src, stats):
    _plot = src.PlotBivariateFeatures(WorldFactbook_Dataset_Clean,gdp,internet_percent,False)

    _result = stats.pearsonr(WorldFactbook_Dataset_Clean[gdp],WorldFactbook_Dataset_Clean[internet_percent])
    print(f"P-value of Pearson Correlation Test: {_result.pvalue:.4f}")

    _plot
    return


@app.cell
def _(mo):
    mo.md(r"# 5. Relationship Between `gdp` and `internet_percent` by Type of Income")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Repeating the use of Pearson Correlation Test, it is shown that there is a significant correlation when income is medium and high, due to how GDP values accumulate in these two categories, which are at high `internet_percent` values. The fact that there is no significant correlation when income is low can be related to the fact that countries are shown to be uniformly distributed over the different values of `internet_percent`.
    
        Therefore, it can be said that GDP, from a certain threshold, does have an influence on Internet access but reaches a saturation limit, due to the correlation when there is income (although there is not enough evidence, countries, to affirm this), GDP ceases to have an influence.
        """
    )
    return


@app.cell
def _(
    WorldFactbook_Dataset_Clean,
    gdp,
    internet_percent,
    src,
    stats,
    type_income,
):
    _plot = src.PlotHueBivariateFeatures(WorldFactbook_Dataset_Clean,gdp,internet_percent)

    for _type_income in WorldFactbook_Dataset_Clean[type_income].unique():
        _data = WorldFactbook_Dataset_Clean.query(f"{type_income} == '{_type_income}'")
        _result = stats.pearsonr(_data[gdp],_data[internet_percent])
        print(f'{' '.join(map(str.capitalize,_type_income.split('-')))}')
        print(f"P-value of Pearson Correlation Test: {_result.pvalue:.4f}\n")

    _plot
    return


@app.cell
def _(mo):
    mo.md(r"# Conclusions")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The most fundamental part of any Exploratory Data Analysis is based on generating new knowledge based on answering questions by means of statistics, both the use of graphs and appropriate tests. Both ideas were used to generate the exhibits in addition to taking care of the general aesthetics of the created plots, always keeping in mind that the information to be presented is communicated.
    
        Finally, what I take most from this project is the way in which the information and data has to be presented or exposed in order to reach the objective of the communication.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"# References")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        * [1] [Proyecto 3: *Web Scraping con Scrapy*](../RequirementsDocument.pdf). Tinoco Martinez Sergio Rogelio
        * [2] DataFrame. Pandas. https://pandas.pydata.org/docs/reference/frame.html
        * [3] API Reference. Numpy. https://numpy.org/doc/stable/reference/index.html
        * [4] API reference. Seaborn. https://seaborn.pydata.org/api.html
        * [5] API Reference. Matplotlib. https://matplotlib.org/stable/api/index.html
        * [6] Statistical functions. SciPy. https://docs.scipy.org/doc/scipy/reference/stats.html
        * [7] API Reference. Marimo. https://docs.marimo.io/api/
        """
    )
    return


if __name__ == "__main__":
    app.run()
