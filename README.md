# Web Scrapping of The World Factbook Website
## Abstract
The aim of this project is to perform Web Scrapping to the CIA's The World Factbook page in order to obtain relevant country data and perform a statistical analysis to show the relationship between GDP and percentage of Internet users.

## Author, Affiliation and Contact
Alexis Aguilar [Student of Bachelor's Degree in "Tecnologías para la Información en Ciencias" at Universidad Nacional Autónoma de México [UNAM](https://www.unam.mx/)]: alexis.uaguilaru@gmail.com

Project developed for the subject "Sociedad de la Información, del Conocimiento y del Aprendizaje" (Data Science Introduction) for the class taught in semester 2025-2.

## License
Project under [MIT License](LICENSE)

## Introduction
Web Scrapping becomes a valuable tool for obtaining data from different sources such as web pages, as well as to create datasets that will be used to train Machine Learning models. They can also be used for data analysis in order to generate new knowledge.

Among the factors that influence a country's Gross Domestic Product (GDP) are those related to technological progress and its availability in society, among people, with the number of Internet users being the main technological factor. Therefore, it is essential to study the relationship between this technological service and the purchasing power of a country.

## General Aim
The purpose of this project is to practice obtaining data through Web Scrapping from [The World Factbook](https://www.cia.gov/the-world-factbook/countries/) and to analyze the relationship between GDP and the percentage of Internet users in a country. In addition to achieving this purpose, the requirements in [[1]](#references) are also followed.

## Web Scraping
Two difficulties were encountered when performing Web Scraping of [The World Factbook](https://www.cia. gov/the-world-factbook/countries/), which may be related to my little experience in using Scrapy and Web Scraping, but they were related: one is the waiting time before running the Scrapy spider, that is, the page needed to load the data from a JSON file that was requested by JavaScript, then it was required to wait some time before; and the other is related to the fact that the website, apparently, detects when running requests with headless browsers, that is, it could not get the data to extract if it was not opened from a browser. For both problems and based on the Scrapy documentation [[2]](#references), it is suggested to use Playwright and, specifically, the [integration with Scrapy](https://github.com/scrapy-plugins/scrapy-playwright). 

And once the Scrapy-Playwright integration is done, it can proceed with the web scraping itself where the Items objects were used to store the different data requested from the countries according to the guidelines in [[1]](#references) and the Pipelines processes for the preliminary processing of the data and to download the images of the flags of the different countries.

The obtained dataset, even with missing values and without manual corrections applied, is available in [Dataset_Raw](./Dataset/Dataset_Raw.csv) and in the same folder are the images obtained from the countries with their flag images.

## Data Wrangling
The process related to Data Wrangling can be found in the notebook based on [Marimo](./DataWrangling/DataWrangling.py) or in the one based on [Jupyter](./DataWrangling/DataWrangling.ipynb). In these notebooks the ideas and processes for the treatment of missing values are exposed where the information and knowledge acquired during the [Web Scraping](#web-scraping) process is used to determine the values to be imputed (in most cases, they were missing values associated to islands or projected zones).

## Exploratory Data Analysis
The process related to Exploratory Data Analysis can be consulted in the notebook based on [Marimo](./ExploratoryDataAnalysis/ExploratoryDataAnalysis.py) or in the one based on [Jupytre](./ExploratoryDataAnalysis/ExploratoryDataAnalysis.ipynb). In these notebooks, the answers to the questions in [[1]](#references) about the relationship between GDP and the percentage of users with Internet access in a country are presented by means of graphs and hypothesis testing. In which it is concluded that they are related in a global way, when using the data according to the type of income, this relationship changes.

## Usage and Installation
First the repository has to be cloned using the following command:
```bash
git clone https://github.com/alexisuaguilaru/WebScraping_CIAFactbook
```
And, preferably in a Python environment, install the libraries required to run all the scripts and libraries used in this project:
```bash
pip install -r requirements.txt
```
### Web Scraping
In order to run the web scraping process, it is necessary to additionally install the drivers of a web browser that will be used by [Playwright](https://github.com/scrapy-plugins/scrapy-playwright), this is done with:
```bash
playwright install chromium
```
Finally, to execute the project spiders, the following command is used:
```bash
scrapy crawl CountryInformation
```
### Usage of Marimo Notebooks
To start using the notebooks based on [Marimo](https://github.com/marimo-team/marimo), use one of the following commands depending on the notebook to be opened for inspection (it must be in the root of the project):
```bash
marimo run DataWrangling/DataWrangling.py
marimo run ExploratoryDataAnalysis/ExploratoryDataAnalysis.py
```
And to be able to edit them (and being in the root of the project) it is made use of one of the following commands according to the case:
```bash
marimo edit DataWrangling/DataWrangling.py
marimo edit ExploratoryDataAnalysis/ExploratoryDataAnalysis.py
```
### Usage of Jupyter Notebooks
Typical commands are used to open a Jupyter notebook, and depending on the user's preferences, this can be done with the following commands depending on the notebook of interest:
```bash
jupyter lab DataWrangling/DataWrangling.ipynb
jupyter lab ExploratoryDataAnalysis/ExploratoryDataAnalysis.ipynb
```

## Conclusions
The main learning that I took from this project is how to use Scrapy, or better to know a little about how it works, doing this project allowed me to know how you can structure a web scraping project using a dedicated framework for this. Not only was learning Scrapy pure, but also one of its plugins, Scrapy-Playwright, to generate a direct interaction with the pages and simulate that the spider is a real user, this allows to exploit all the qualities offered by Scrapy to the maximum while automating the extraction of data from web pages in a simple way.

Therefore, knowing how Scrapy works becomes a very versatile and useful tool for the generation of new datasets from which to generate new knowledge and ideas or, mainly, to train new and more sophisticated Artificial Intelligence models.

## References
* [1] [Proyecto Web Scraping con Scrapy](RequirementsDocument.pdf). Tinoco Martinez Sergio Rogelio
* [2] Scrapy 2.13 documentation. Scrapy developers. https://docs.scrapy.org/en/2.13/