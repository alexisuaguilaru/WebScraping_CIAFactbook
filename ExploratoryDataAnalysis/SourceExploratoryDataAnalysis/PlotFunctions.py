import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.axes import Axes


PrettyFeatureNames = {
    'gdp' : 'GDP',
    'internet_percent' : 'Internet Users Percent',
    'gdp_encode' : 'Type of Income'
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
    fig , axes = plt.subplots(figsize=(10,8),layout='tight')

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
    
    Axes.tick_params(size=12,width=2,labelsize=20)

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
        Figure where the plot was plotted 
    """
    fig , axes = CreatePlot()

    _feature_name = PrettyFeatureNames[Feature]
    if Log10:
        _data = np.log10(Dataset[[Feature]])
        _x_label = r'$log_{10}$'+f'({_feature_name})'
    else:
        _data = Dataset[[Feature]]
        _x_label = f'{_feature_name}'
    
    sns.violinplot(data=_data,x=Feature,ax=axes,
                   color=BaseColor,fill=False,
                   linewidth=4,inner='box',
                   inner_kws={'box_width':36,'whis_width':6})

    _title_fig = f'Distribution of {_feature_name}'
    SetLabels(axes,_title_fig,_x_label)

    return fig