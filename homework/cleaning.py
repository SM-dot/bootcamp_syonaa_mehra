
import pandas as pd
import numpy as np

def drop_missing(df: pd.DataFrame, threshold: float = 0.6) -> pd.DataFrame:
    """Drop columns whose fraction of missing values is >= threshold."""
    frac_missing = df.isna().mean()
    to_drop = frac_missing[frac_missing >= threshold].index.tolist()
    return df.drop(columns=to_drop), to_drop

def fill_missing_median(df: pd.DataFrame, cols):
    """Fill missing numeric values in `cols` with the column median."""
    df = df.copy()
    for c in cols:
        if c in df.columns:
            if pd.api.types.is_numeric_dtype(df[c]):
                median = df[c].median()
                df[c] = df[c].fillna(median)
            else:
                raise TypeError(f"Column {c} is not numeric; cannot fill with median.")
    return df

def standardize_cities(df: pd.DataFrame, col: str = 'city', out_col: str = 'city_clean') -> pd.DataFrame:
    df = df.copy()
    mapping = {
        'nyc': 'New York',
        'new york': 'New York',
        'new york city': 'New York',
        'ny': 'New York',
        'san francisco': 'San Francisco',
        'sf': 'San Francisco',
        'sfo': 'San Francisco',
        'san fran': 'San Francisco',
        'los angeles': 'Los Angeles',
        'la': 'Los Angeles',
        'chicago': 'Chicago',
        'chi-town': 'Chicago',
    }
    def normalize(v):
        if pd.isna(v):
            return v
        key = str(v).strip().lower()
        return mapping.get(key, v if isinstance(v, str) else str(v))
    df[out_col] = df[col].apply(normalize)
    return df

def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates().reset_index(drop=True)

def normalize_data(df: pd.DataFrame, cols, suffix: str = '_scaled'):
    df = df.copy()
    for c in cols:
        if c in df.columns and pd.api.types.is_numeric_dtype(df[c]):
            mn, mx = df[c].min(), df[c].max()
            if pd.isna(mn) or pd.isna(mx) or mx == mn:
                df[c + suffix] = 0.0
            else:
                df[c + suffix] = (df[c] - mn) / (mx - mn)
    return df
