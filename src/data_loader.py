"""Fetch and cache datasets from the Ken French Data Library."""

import os
import pandas as pd
import pandas_datareader.data as web

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)


def get_french(name: str, start: str = "1963-07", end: str = "2024-12") -> pd.DataFrame:
    """Download a Ken French dataset, cache locally as parquet.

    Parameters
    ----------
    name : str
        Dataset name exactly as listed on the French library.
        Common ones:
          - "F-F_Research_Data_Factors"          (Mkt-RF, SMB, HML, RF)
          - "F-F_Research_Data_5_Factors_2x3"    (adds RMW, CMA)
          - "F-F_Momentum_Factor"                (Mom / WML)
          - "25_Portfolios_5x5"                  (test portfolios)
    start, end : str
        "YYYY-MM" bounds for monthly data.

    Returns
    -------
    pd.DataFrame with a DatetimeIndex (month-end) and returns in percent.
    """
    cache_path = os.path.join(DATA_DIR, f"{name}.parquet")

    if os.path.exists(cache_path):
        df = pd.read_parquet(cache_path)
    else:
        raw = web.DataReader(name, "famafrench", start=start, end=end)
        # raw is a dict; table 0 is always the monthly data
        df = raw[0]
        df.index = df.index.to_timestamp(how="end")
        df.to_parquet(cache_path)

    # Filter to requested range
    df = df.loc[start:end]
    return df
