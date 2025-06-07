import pandas as pd

from typing import Any

def FillMissingValues(Dataset:pd.DataFrame,Feature:str,FillingValue:Any) -> pd.Series:
    """
    Function for filling the missing values in a 
    feature of a dataset with a constant value

    Parameters
    ----------
    Dataset : pd.DataFrame
        Dataset in which is being filled its missing values
    Feature : str
        Feature with missing values
    FillingValue : Any
        Value with which the missing values are being filled

    Returns
    -------
    filled_dataset : pd.Series
        Serie without missing values in `Feature`
    """
    filled_dataset = Dataset[Feature].copy()
    missing_values_entry = filled_dataset != filled_dataset

    filled_dataset.loc[missing_values_entry] = FillingValue
    return filled_dataset