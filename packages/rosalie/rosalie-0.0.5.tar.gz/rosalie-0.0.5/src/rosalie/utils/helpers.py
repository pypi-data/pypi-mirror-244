import os
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pandas as pd
import pandas_gbq
from IPython.display import display


def data_info(df):
    id_col = df.columns[df.columns.str.contains("id")]
    date_col = df.columns[df.columns.str.contains("date|time")]
    print(f"Shape: {df.shape}")
    print(f"Units: {df[id_col[0]].nunique():,}")
    if len(date_col) > 0:
        print(f"Periods: {df[date_col[0]].nunique():,}")
    display(df.head())


def _query_data(
    query,
    project_id="just-data-expenab-dev",
    cache_path=None,
    convert_dates=None,
):
    """Query data from GBC or read from disk (for testing).

    Arguments:
    ----------
    query : string
        A valid BigQuery query.
    project_id : string, default "just-data-bq-users"
        Project ID to be used for query.
    cache_path: string, filepath of parquet file, default None
        Filepath to write query to (if file doesn't exist)
        or read query from (if file does exist).
    convert_dates : list of strings, default None
        List of columns to convert to datetime.
    """
    if cache_path is not None:
        if not cache_path.endswith(".parquet"):
            raise ValueError("Filepath must end with '.parquet'.")
        if os.path.isfile(cache_path):
            print("Reading data from cache...")
            result = pd.read_parquet(cache_path)
            return result

    print("Querying data from BigQuery...")
    result = pd.read_gbq(query, project_id=project_id)

    if convert_dates is not None:
        # Convert dates to datetime so that they can be written to parquet
        result[convert_dates] = result[convert_dates].apply(pd.to_datetime)
    else:
        mask = result.columns.str.contains("date|time")
        date_cols = result.columns[mask]
        result[date_cols] = result[date_cols].apply(pd.to_datetime)

    if cache_path is not None:
        print("Writing data to cache...")
        result.to_parquet(cache_path, index=False)

    return result


def read_data(level="customer", query_kwargs=None):
    """
    Read data for experiment evaluation.

    Arguments:
    ----------
    level : string, default "customer"
        Level of data to read. One of {"customer", "restaurant", "city"}.
    query_kwargs : dict, default None
        Keyword arguments to pass to _query_data.
    """
    if query_kwargs is None:
        query_kwargs = {}
    query = open(f"rosalie/sql/{level}.sql").read()
    filepath = f"/Users/fabian.gunzinger/tmp/expev-{level}.parquet"
    df = _query_data(query, cache_path=filepath, **query_kwargs).set_index(
        "timeframe", drop=False
    )
    return df


def add_pre_metric_value(
    df: pd.DataFrame,
    metric: str,
    pre_period: Tuple[str, str],
    post_period: Tuple[str, str],
    output_fmt: str = "cross_section",
    id_col: str = None,
):
    """Add pre-period metric value for CUPED adjustment.

    Arguments:
    ----------
    df : pd.DataFrame
        Dataframe to add pre-period metric value to.
    metric : string
        Name of metric column.
    pre_period : tuple of strings
        Start and end date of pre-period.
    post_period : tuple of strings
        Start and end date of post-period.
    output_fmt : string, default 'cross_section'
        Format of output. One of {'cross_section', 'panel'}.
    id_col : string, default None
        Name of id column.

    Returns:
    --------
    result : pd.DataFrame
        Dataframe with pre-period metric value added.
    """
    if id_col is None:
        mask = df.columns.str.startswith("id") | df.columns.str.endswith("id")
        id_col = df.columns[mask][0]

    pre = (
        df.loc[slice(*pre_period)]
        .groupby(id_col)[metric]
        .mean()
        .astype("float32")
        .rename(f"{metric}_pre")
        .reset_index()
    )

    if output_fmt == "cross_section":
        post = (
            df.loc[slice(*post_period)]
            .groupby(id_col)[metric]
            .mean()
            .astype("float32")
            .reset_index()
        )
    else:
        cols = [id_col, "timeframe", metric]
        post = (
            df.loc[slice(*post_period), cols]
            .reset_index(drop=True)
            .sort_values(cols[:2])
        )
    result = pd.merge(post, pre, how="left", on=id_col).dropna()
    return result


def preprocess_data(df):
    """Clean dataframe."""

    # Dates to datetime
    df["timeframe"] = pd.to_datetime(df["timeframe"])

    # Keep valid IDs only
    df = df[df["id"].str.startswith("JE:UK")]

    # Drop missing values
    df = df.dropna()

    return df


def select_sample(df, num_units=None, num_periods=None, seed=2312):
    """Select sample from dataframe.

    Arguments:
    ----------
    df : pd.DataFrame
        Dataframe to sample from.
    num_units : int, default None
        Number of units to sample. If None, all units are included.
    num_periods : int, default None
        Number of periods to sample. If None, all periods are included.
    seed : int, default 2312
        Random seed to use for sampling.

    Returns:
    --------
    df : pd.DataFrame
        Sampled dataframe.
    """
    if num_units is None:
        units = df["id"].unique()
    else:
        rng = np.random.default_rng(seed)
        units = rng.choice(df["id"].unique(), size=num_units, replace=False)

    if num_periods is None:
        periods = sorted(df["timeframe"].unique())
    else:
        periods = periods[:num_periods]

    return df[df["id"].isin(units) & df["timeframe"].isin(periods)]


def make_sample_data(
    units=100_000,
    periods=50,
    max_unit_effect=0.1,
    metric_name="y",
    add_assignment=False,
    cross_section=False,
    default_panel=False,
    default_cross_section=False,
):
    """Create dummy data for testing.

    Arguments:
    ----------
    units : int
        Number of units to simulate.
    periods : int
        Number of periods to simulate.
    max_unit_effect : float
        Size of unit effect to simulate. This is useful, for instance, to ensure that
        CUPED has an effect.
    metric_name : str
        Name of metric column.
    add_assignment : bool
        Whether to add assignment columns.
    cross_section : bool
        Whether to return cross-sectional data.

    Returns:
    --------
    df : pd.DataFrame
        Simulated data.
    """
    n = units * periods
    date_range = list(pd.date_range("2023-01-01", periods=periods, freq="D"))
    unit_effect = np.random.uniform(0, max_unit_effect, size=n)

    df = pd.DataFrame(
        {
            "id": sorted([f"unit_{id}" for id in range(units)] * periods),
            "timeframe": date_range * units,
            metric_name: np.random.uniform(0, 1, size=n) + unit_effect,
        }
    )

    if add_assignment:
        labs = {False: "control", True: "treatment"}
        df["is_treated"] = np.random.choice([0, 1], size=n).astype(bool)
        df["assignments"] = df["is_treated"].map(labs)
        df["assignments_freq"] = 1

    if cross_section:
        df = df.drop(columns="timeframe").groupby("id").mean().reset_index()

    return df


def traditional_cuped(df, metric):
    """Run traditional CUPED and return p-value."""

    def _cuped_adjusted_metric(df, metric, metric_pre):
        dd = df.dropna(subset=[metric, metric_pre])
        m = np.cov([dd[metric], dd[metric_pre]])
        theta = m[0, 1] / m[1, 1]
        y = df[metric]
        x = df[metric_pre]
        return (y - (x - x.mean()) * theta).fillna(y)

    df = df.copy()
    df[metric] = _cuped_adjusted_metric(df, metric, f"{metric}_pre")

    # Perform experiment evaluation and return p-value
    # (Use WLS to be consistent with CausalJet)
    y = df[metric]
    x = sm.add_constant(df["is_treated"].astype(float))
    w = df["assignments_freq"]
    model = sm.WLS(endog=y, exog=x, weights=w)
    results = model.fit()
    return results.pvalues["is_treated"]
