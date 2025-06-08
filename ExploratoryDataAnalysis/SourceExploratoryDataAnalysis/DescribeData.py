import pandas as pd

def DescriptiveAnalysis(Dataset:pd.DataFrame,Feature:str) -> pd.DataFrame:
    """
    Function for creating a basic descriptive 
    statistical for a feature in a dataset

    Parameters
    ----------
    Dataset : pd.DataFrame 
        Feature values with which the descriptive is generated
    Feature : str 
        Feature with which the descriptive is generated

    Returns
    -------
    descriptive : pd.DataFrame
        Descriptive statistical was generated
    """
    return Dataset[[Feature]].describe().loc[['mean','std','25%','50%','75%']]