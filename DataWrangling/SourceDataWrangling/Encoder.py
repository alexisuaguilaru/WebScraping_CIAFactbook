import pandas as pd
import numpy as np

def EncoderGDP(Dataset:pd.DataFrame) -> np.ndarray:
    """
    Function to encode the values of `gdp`
    using the rule described above

    Parameters
    ----------
    Dataset : pd.DataFrame
        Dataset where transformation is applied

    Returns
    -------
    gpd_encode : np.ndarray
        Return a array with the encoded 
        values 
    """
    class_values = np.array([5000,25000])
    class_names = np.array([border_name+'-income' for border_name in ['low','average','high']])

    class_indexes = class_values.searchsorted(Dataset['gdp'])
    return class_names[class_indexes]