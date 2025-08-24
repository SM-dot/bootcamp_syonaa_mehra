import pandas as pd
import numpy as np

def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """
    Returns a boolean mask for IQR-based outliers.

    This method assumes the data's distribution can be reasonably summarized
    by its quartiles. The `k` value controls the strictness of the outlier
    detection. A larger k value will flag fewer points as outliers.

    Args:
        series (pd.Series): The pandas Series to analyze.
        k (float): The multiplier for the IQR.

    Returns:
        pd.Series: A boolean Series where True indicates an outlier.
    """
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - k * iqr
    upper_bound = q3 + k * iqr
    return (series < lower_bound) | (series > upper_bound)

def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    """
    Returns a boolean mask for Z-score-based outliers.

    This method assumes a roughly normal distribution. Data points with an
    absolute Z-score greater than the threshold are flagged as outliers.

    Args:
        series (pd.Series): The pandas Series to analyze.
        threshold (float): The Z-score threshold.

    Returns:
        pd.Series: A boolean Series where True indicates an outlier.
    """
    mu = series.mean()
    sigma = series.std(ddof=0)
    z = (series - mu) / (sigma if sigma != 0 else 1.0)
    return z.abs() > threshold

def winsorize_series(series: pd.Series, lower: float = 0.05, upper: float = 0.95) -> pd.Series:
    """
    Clips extreme values in a Series to a specified range (winsorizing).

    This function replaces values below the lower quantile and above the upper
    quantile with the values at those quantiles. This is useful for handling
    outliers without discarding data.

    Args:
        series (pd.Series): The pandas Series to winsorize.
        lower (float): The lower percentile to clip at (e.g., 0.05 for 5th percentile).
        upper (float): The upper percentile to clip at (e.g., 0.95 for 95th percentile).

    Returns:
        pd.Series: The winsorized pandas Series.
    """
    lo = series.quantile(lower)
    hi = series.quantile(upper)
    return series.clip(lower=lo, upper=hi)