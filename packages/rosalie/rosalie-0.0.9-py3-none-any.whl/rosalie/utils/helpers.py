import numpy as np
import pandas as pd


def data_info(df):
    """Print basic information about dataframe."""
    id_col = df.columns[df.columns.str.contains("id")]
    date_col = df.columns[df.columns.str.contains("date|time")]
    print(f"Shape: {df.shape}")
    print(f"Units: {df[id_col[0]].nunique():,}")
    if len(date_col) > 0:
        print(f"Periods: {df[date_col[0]].nunique():,}")
    print(df.head())


def add_artificial_gmw(df):
    df["gmv"] = np.random.normal(25, 5, size=len(df))
    return df
