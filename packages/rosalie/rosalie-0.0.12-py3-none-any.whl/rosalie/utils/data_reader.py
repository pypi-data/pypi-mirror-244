import os
from typing import Optional

import pandas as pd

QUERIES = {
    # Using Ireland data for customer data because it's familiar
    # from IE OneWeb rollout
    "customer": """
        SELECT
        v.visit_key,
        v.user.consolidated_user_id AS user_id,
        v.visit_date AS timeframe,
        v.app AS platform,
        o.order_price,
        FROM
        `just-data-warehouse.analytics.visits_ie_*` AS v
        LEFT JOIN
        UNNEST(orders) AS o
        WHERE
        visit_date BETWEEN "2023-01-01" AND "2023-08-31"
        AND totals.pageviews > 0
        AND totals.pageviews IS NOT NULL
        """,
    "restaurant": """
        SELECT
        id,
        timeframe,
        menu_2_basket_cvr,
        avg_food_price
        FROM
        `just-data-warehouse.experimentation.causal_jet_metrics_resto_je_uk`
        WHERE
        frequency = "daily"
        AND timeframe between "2023-01-01" AND "2023-06-30"
        """,
    "city": """
        SELECT
        timeframe,
        restaurant_city as id,
        orders,
        avg_food_price,
        revenue,
        revenue_per_order
        FROM
        `just-data-warehouse.experimentation.causal_jet_metrics_city_je_uk`
        WHERE
        frequency = "daily"
        AND timeframe BETWEEN "2023-01-01" AND "2023-06-30"
        """,
}


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
        if (cache_path is not None) and os.path.isfile(cache_path):
            print("Reading data from cache...")
            result = self._read_from_cache(cache_path)
        else:
            print("Querying data from BigQuery...")
            result = self._query_from_bigquery(QUERIES[level], cache_path)
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
