import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.axes import Axes


PrettyFeatureNames = {
    'gdp' : 'GDP',
    'internet_percent' : 'Internet Users Percent',
    'gdp_encode' : 'Type of Income',
    'low-income' : 'Low Income',
    'average-income' : 'Average Income',
    'high-income' : 'High Income',
}

InverseTypeIncome = {
    'low-income' : 0,
    'average-income' : 1,
    'high-income' : 2,
}

BaseColor = '#4169e1' 
BasePalette = ['#B24020','#F7D458','#2CA02C']


def CreatePlot() -> tuple[Figure,Axes]:
    """
    Function for create base plotting 
    with custom configuration

    Returns
    -------
    fig : Figure 
    axes : Axes
    """
    fig , axes = plt.subplots(subplot_kw={'frame_on':False},figsize=(10,8),layout='tight')

    return fig , axes

def SetLabels(Axes:Axes,Title:str=None,X_Label:str=None,Y_Label:str=None) -> None:
    """
    Function for setting labels in a axes 
    with certain names

    Parameters
    ----------
    Axes : Axes
        Axes in which setting axis labels is applied
    Title : str
        Title for the axis
    X_Label : str
        x axis' label
    Y_Label : str
        y axis' label
    """
    if Title:
        Axes.set_title(Title,size=32)
    if X_Label:
        Axes.set_xlabel(X_Label,size=24)
        Axes.xaxis.offsetText.set_fontsize(20)
    if Y_Label:
        Axes.set_ylabel(Y_Label,size=24)
    
    Axes.tick_params(size=12,width=0,labelsize=20)

def FormatLabel(Feature:str,Log10:bool) -> str:
    """
    Function for formatting the label of 
    an axis based on its scale

    Parameters
    ----------
    Feature : str
        Feature is being formatted
    Log10 : bool
        Whether its scale is log_10

    Returns
    -------
    _label : str
        Formatted label
    """
    _feature_name = PrettyFeatureNames[Feature]
    if Log10:
        _label = r'$log_{10}$'+f'({_feature_name})'
    else:
        _label = f'{_feature_name}'

    return _label

def PlotUnivariateFeature(Dataset:pd.DataFrame,Feature:str,Log10:bool=True) -> Figure:
    """
    Functions for plotting the feature values 
    of a dataset with log_10 scale optional

    Parameters
    ----------
    Dataset : pd.DataFrame
        Dataset whose data is plotted 
    Feature : str
        Feature which is plotted
    Log10 : bool
        Whether is applied log_10 transformation to the values

    Returns
    -------
    fig : Figure
        Figure where the plot was generated
    """
    fig , axes = CreatePlot()

    _feature_name = PrettyFeatureNames[Feature]
    if Log10:
        _data = np.log10(Dataset[[Feature]])
    else:
        _data = Dataset[[Feature]]
    _x_label = FormatLabel(Feature,Log10)
    
    sns.violinplot(data=_data,x=Feature,ax=axes,
                   color=BaseColor,fill=False,
                   linewidth=4,inner='box',
                   inner_kws={'box_width':36,'whis_width':6})

    _title_fig = f'Distribution of {_feature_name}'
    SetLabels(axes,_title_fig,_x_label)

    axes.grid(axis='x',visible=True,linestyle='--',linewidth=1,alpha=0.75)

    return fig

def PlotBivariateFeatures(Dataset:pd.DataFrame,Feature_X:str,Feature_Y:str,Log10_X:bool=True,Log10_Y:bool=False) -> Figure:
    """
    Function for plotting the relation between two 
    features and their linear regression

    Parameters
    ----------
    Dataset : pd.DataFrame
        Dataset whose data is plotted 
    Feature_X : str
        Feature which is plotted on axis X
    Feature_Y : str
        Feature which is plotted on axis Y
    Log10_X : bool
        Whether is applied log_10 transformation to the values of `Feature_X`
    Log10_Y : bool
        Whether is applied log_10 transformation to the values of `Feature_Y`

    Returns
    -------
    fig : Figure
        Figure where the plot was generated
    """
    fig , axes = CreatePlot()

    _data = Dataset[[Feature_X,Feature_Y]].copy()
    for _log10 , _feature in zip([Log10_X,Log10_Y],[Feature_X,Feature_Y]):
        if _log10: _data[_feature] = np.log10(_data[_feature])

    sns.regplot(data=_data,x=Feature_X,y=Feature_Y,ax=axes,
                color=BaseColor,
                scatter_kws={'s':128,'alpha':0.4},
                line_kws={'lw':8},)

    _x_label = FormatLabel(Feature_X,Log10_X)
    _y_label = FormatLabel(Feature_Y,Log10_Y)

    _title_fig = f'Correlation Between {PrettyFeatureNames[Feature_X]} and\n{PrettyFeatureNames[Feature_Y]}'
    SetLabels(axes,_title_fig,_x_label,_y_label)

    axes.grid(axis='both',visible=True,linestyle='--',linewidth=1,alpha=0.25)

    return fig

def PlotHueBivariateFeatures(Dataset:pd.DataFrame,Feature_X:str,Feature_Y:str,Log10_X:bool=False,Log10_Y:bool=False) -> Figure:
    """
    Function for plotting the relation between two 
    features and their linear regression based on 
    a criterion defined by `gpd_encode` values

    Parameters
    ----------
    Dataset : pd.DataFrame
        Dataset whose data is plotted 
    Feature_X : str
        Feature which is plotted on axis X
    Feature_Y : str
        Feature which is plotted on axis Y
    Log10_X : bool
        Whether is applied log_10 transformation to the values of `Feature_X`
    Log10_Y : bool
        Whether is applied log_10 transformation to the values of `Feature_Y`

    Returns
    -------
    fig : Figure
        Figure where the plot was generated
    """
    fig , axes = CreatePlot()

    _hue = 'gdp_encode'
    _data = Dataset[[_hue,Feature_X,Feature_Y]].copy()
    for _log10 , _feature in zip([Log10_X,Log10_Y],[Feature_X,Feature_Y]):
        if _log10: _data[_feature] = np.log10(_data[_feature])

    for _class in Dataset[_hue].unique():
        _stratified_data = _data.query(f"{_hue} == '{_class}'")
        sns.regplot(data=_stratified_data,x=Feature_X,y=Feature_Y,ax=axes,
                    color=BasePalette[InverseTypeIncome[_class]],label=PrettyFeatureNames[_class],
                    scatter_kws={'s':128,'alpha':0.4},
                    line_kws={'lw':4},)

    _x_label = FormatLabel(Feature_X,Log10_X)
    _y_label = FormatLabel(Feature_Y,Log10_Y)

    _title_fig = f'Correlation Between {PrettyFeatureNames[Feature_X]} and\n{PrettyFeatureNames[Feature_Y]} by Type of Income'
    SetLabels(axes,_title_fig,_x_label,_y_label)

    axes.legend(title=PrettyFeatureNames[_hue],loc='lower right',fontsize=18,title_fontsize=20)
    axes.grid(axis='both',visible=True,linestyle='--',linewidth=1,alpha=0.25)

    return fig