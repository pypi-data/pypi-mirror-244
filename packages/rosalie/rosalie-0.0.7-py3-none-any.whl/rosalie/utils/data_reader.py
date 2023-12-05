import os
from typing import Optional

import pandas as pd


class DataReader:
    """
    Read data for experiment evaluation.

    Arguments:
    ----------
    project_id : string, default "just-data-expenab-dev"
        BigQuery project ID.
    """

    def __init__(
        self,
        project_id: str = "just-data-expenab-dev",
    ):
        self.project_id = project_id

    def load_data(
        self,
        level="customer",
        cache_path: Optional[str] = None,
    ):
        """
        Read data for experiment evaluation.

        Arguments:
        ----------
        level : string, default "customer"
            Level of data to read. One of {"customer", "restaurant", "city"}.
        """
        if os.path.isfile(cache_path):
            print("Reading data from cache...")
            result = self._read_from_cache(cache_path)
        else:
            print("Querying data from BigQuery...")
            query = open(f"rosalie/sql/{level}.sql").read()
            result = self._query_from_bigquery(query, cache_path)
            print("Writing data to cache...")
            self._write_to_cache(result, cache_path)

        self._convert_dates(result)
        return result.set_index("timeframe", drop=False)

    def _read_from_cache(self, filepath: str) -> pd.DataFrame:
        return pd.read_csv(filepath)

    def _query_from_bigquery(self, query: str, cache_path: str) -> pd.DataFrame:
        return pd.read_gbq(query, project_id=self.project_id)

    def _write_to_cache(self, df: pd.DataFrame, cache_path: str) -> pd.DataFrame:
        self._convert_dates(df)
        if not cache_path.endswith(".csv"):
            raise ValueError("Filepath must end with '.csv'.")
        print("Writing data to cache...")
        df.to_csv(cache_path, index=False)

    def _convert_dates(self, df):
        date_cols = df.columns[df.columns.str.contains("date|time")]
        if not date_cols.empty:
            df[date_cols] = df[date_cols].apply(pd.to_datetime)
