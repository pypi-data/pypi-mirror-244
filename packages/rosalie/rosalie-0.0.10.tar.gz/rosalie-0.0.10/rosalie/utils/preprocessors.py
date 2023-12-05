from typing import List, Tuple

import pandas as pd


def create_pre_post_data(
    df: pd.DataFrame,
    id_col: str,
    metrics: List[str],
    pre_period: Tuple[str, str],
    post_period: Tuple[str, str],
    time_col: str = "timeframe",
    output_fmt: str = "cross_section",
):
    """Aggregates data to pre- and post-periods.

    Arguments:
    ----------
    df : pd.DataFrame
        Dataframe to aggregate.
    id_col : string
        Name of id column.
    metrics : list of strings
        Names of metric columns to be aggregated.
    pre_period : tuple of strings
        First and last date of pre-period.
    post_period : tuple of strings
        First and last date of post-period.
    time_col : string, default 'timeframe'
        Name of time column.
    output_fmt : string, default 'cross_section'
        Format of output. One of {'cross_section', 'panel'}.

    Returns:
    --------
    result : pd.DataFrame
        Dataframe with pre-period metric value added.
    """

    # df = df.set_index(time_col)

    pre = (
        df.loc[slice(*pre_period)]
        .groupby(id_col)[metrics]
        .mean()
        .astype("float32")
        .rename(columns=lambda x: f"{x}_pre")
        .reset_index()
    )

    if output_fmt == "cross_section":
        post = (
            df.loc[slice(*post_period)]
            .groupby(id_col)[metrics]
            .mean()
            .astype("float32")
            .reset_index()
        )
    else:
        if time_col not in df.columns:
            raise ValueError(f"Time column '{time_col}' not in dataframe.")
        cols = [id_col, time_col, metrics]
        post = (
            df.loc[slice(*post_period), cols]
            .reset_index(drop=True)
            .sort_values(cols[:2])
        )

    result = pd.merge(post, pre, how="left", on=id_col).dropna()
    return result
