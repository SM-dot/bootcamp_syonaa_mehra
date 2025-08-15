# src/utils.py
import pandas as pd

def get_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates and returns descriptive statistics for a pandas DataFrame.
    """
    return df.describe()