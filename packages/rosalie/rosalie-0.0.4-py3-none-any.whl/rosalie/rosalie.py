from collections import defaultdict, namedtuple
from concurrent.futures import ProcessPoolExecutor
from copy import copy
from dataclasses import dataclass
from multiprocessing import cpu_count

import altair as alt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.weightstats import ttest_ind
from tqdm import tqdm


class Result:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def get_data(self):
        """Return dataframe with simulation results."""
        return self.data

    def _single_plot(
        self,
        data,
        x="sample_size",
        y="power",
        title=None,
        color="evaluator",
        hline_pos="0.8",
    ):
        """Print a power graph.

        Parameters
        ----------
        data : dataframe (required)
            name of dataframe
        x : string (optional)
            name of x coordinate (sample size), default is 'sample_size'
        y : string (optional)
            name of y coordinate (power), default is 'power'
        color : string (optional)
            name of variable for color encoding, default is 'test'
        hline_pos : str of float (optional)
            position of horizontal line to indicate target power level, default is '0.8'

        Returns
        -------
        Altair plot: A plot showing level of power for each sample size for each evaluator.
        """
        dots = (
            alt.Chart(data)
            .mark_point()
            .encode(
                x=alt.X(x, axis=alt.Axis(title="Sample size")),
                y=alt.Y(y, axis=alt.Axis(title="Power")),
                color=alt.Color(color, legend=alt.Legend(title="Evaluator")),
            )
        )
        loess = dots.transform_loess(x, y, groupby=[color]).mark_line()
        hline = (
            alt.Chart(self.data)
            .mark_rule(color="red")
            .encode(
                y=alt.Y("a:Q", axis=alt.Axis(title="")),
            )
            .transform_calculate(a=hline_pos)
        )
        plot = dots + loess + hline
        if title:
            plot = plot.properties(title=title)
        return plot

    def plot(self):
        mdes_values = self.data["mdes"].unique()
        plots = []
        for mdes in mdes_values:
            data = self.data[self.data["mdes"] == mdes]
            plot = self._single_plot(
                data,
                title=f"Minimum detectable effect size: {mdes}%",
            )
            plots.append(plot)
        return alt.vconcat(*plots)


ExperimentResult = namedtuple(
    "ExperimentResult", ["preprocessor", "evaluator", "sample_size", "mdes", "power"]
)


class Evaluator:
    """
    Class to simulate experiments.

    Attributes:
    ----------
    df : pd.DataFrame
        Dataframe to sample from.
    preprocessors : list, default []
        List of callables to apply to the data before sampling. Each callable
        should take a dataframe as input and return a dataframe as output.
    evaluators : list, default []
        List of callables to use for experiment evaluation. Each callable
        should take a dataframe as input and return a p-value as output.
    sample_min : int, default 100_000
        Minimum sample size to simulate.
    sample_max : int, default 200_000
        Maximum sample size to simulate.
    step_size : int, default 10_000
        Step size for sample size.
    mdes : float, default 1
        Minimum detectable effect size (in percentage points).
    num_runs : int, default 100
        Number of times to run each experiment.
    sample_timestamps : bool, default False
        If True, sample periods instead of units.
    alpha : float, default 0.05
        Significance level.
    metric : str, default 'y'
        Name of metric column.
    random_seed : int, default 2312
        Random seed to use for sampling.
    use_default_preprocessor : bool, default False
        If True, use default preprocessor.
    use_default_evaluator : bool, default False
        If True, use default evaluator.
    id_col : str, default 'id'
        Name of id column.
    testing : bool, default False
        If True, print evaluator results.
    """

    def __init__(
        self,
        df,
        evaluators=None,
        sample_min=100_000,
        sample_max=200_000,
        num_steps=10,
        mdes=2,
        num_runs=100,
        sample_timestamps=False,
        alpha=0.05,
        metric="y",
        random_seed=2312,
        baseline_evaluator=None,
        id_col="id",
        testing=False,
        preprocessors=None,
    ):
        self.df = df
        self.evaluators = evaluators or []
        self.preprocessors = preprocessors or []
        self.sample_min = sample_min
        self.sample_max = sample_max
        self.num_steps = num_steps
        self.mdes = mdes
        self.num_runs = num_runs
        self.sample_timestamps = sample_timestamps
        self.alpha = alpha
        self.metric = metric
        self.random_seed = random_seed
        self.baseline_evaluator = baseline_evaluator
        self.id_col = id_col
        self.testing = testing

        self.has_preprocessors = len(self.preprocessors) > 0

        if not self.has_preprocessors:
            self.preprocessors = copy(self.preprocessors)
            self.preprocessors = [self._empty_preprocessor]

        if baseline_evaluator is not None:
            evaluators = {
                "welch": self._welch_t_test,
                "wls": self._wls,
            }
            self.evaluators = copy(self.evaluators)
            self.evaluators.insert(0, evaluators[self.baseline_evaluator])

        # Input checks
        if self.sample_timestamps:
            assert (
                self.df.timeframe.nunique() >= self.sample_max
            ), "Max sample size cannot be larger than number of time periods in the data."
        else:
            assert (
                len(self.df) >= self.sample_max
            ), "Max sample size cannot be larger than the number of units in the data."

        eval_names = [func.__name__ for func in self.evaluators]
        assert len(eval_names) == len(
            set(eval_names)
        ), "Evaluator names must be unique."

        preproc_names = [func.__name__ for func in self.preprocessors]
        assert len(preproc_names) == len(
            set(preproc_names)
        ), "Preprocessor names must be unique."

        assert len(self.evaluators) > 0, "At least one evaluator must be specified."
        assert (
            self.sample_min <= self.sample_max
        ), "Min sample size cannot be larger than max sample size."

        print(f"Specified evaluators: {self._evaluator_names()}")
        if self.has_preprocessors:
            print(f"Specified preprocessors: {self._preprocessor_names()}")

        self.rng = np.random.default_rng(self.random_seed)

    def _evaluator_names(self):
        """Return names of evaluators."""
        return [func.__name__ for func in self.evaluators]

    def _preprocessor_names(self):
        """Return names of preprocessors."""
        return [func.__name__ for func in self.preprocessors]

    def _empty_preprocessor(self, df):
        """Return unprocessed data."""
        return df

    def _welch_t_test(self, df, metric):
        """Return p-value of Welch's t-test."""
        control_sample = df[df["assignments"] == "control"][metric]
        variant_sample = df[df["assignments"] == "treatment"][metric]
        t, p, df = ttest_ind(control_sample, variant_sample, usevar="unequal")
        return p

    def _wls(self, df, metric):
        """Return p-value of weighted least squares regression."""
        y = df[metric]
        x = sm.add_constant(df["is_treated"].astype(float))
        w = df["assignments_freq"]
        model = sm.WLS(endog=y, exog=x, weights=w)
        results = model.fit()
        return results.pvalues["is_treated"]

    def _create_treatment_assignments(self, df):
        """Add columns with treatment assignments to dataframe."""
        unique_ids = df[self.id_col].unique()
        assignments = self.rng.choice([True, False], size=len(unique_ids))
        labels = {True: "treatment", False: "control"}
        id_to_assignment = dict(zip(unique_ids, assignments))

        df["is_treated"] = df[self.id_col].map(id_to_assignment)
        df["assignments"] = df["is_treated"].map(labels)
        df["assignments_freq"] = 1

        return df

    def _get_result_cols(self):
        """Return names of columns in result dataframe."""
        cols = ["preprocessor", "evaluator", "sample_size", "mdes", "power"]
        if not self.has_preprocessors:
            cols.remove("preprocessor")
        return cols

    def _add_treatment_effect(self, df, metric, mdes):
        """Add column with artificial treatment effect to dataframe."""
        df = df.copy()
        map = {"control": 1.0, "treatment": (1 + mdes / 100)}
        multiplier = df["assignments"].map(map)
        df[metric] = df[metric] * multiplier
        return df

    def _sample_timestamps(self, df, sample_size):
        """Sample timestamps from dataframe."""
        unique_timestamps = sorted(df["timeframe"].unique())
        sample_timestamps = unique_timestamps[:sample_size]
        return df[df["timeframe"].isin(sample_timestamps)].copy()

    def _sample_users(self, df, sample_size):
        """Sample users from dataframe."""
        unique_ids = df[self.id_col].unique()
        sample_ids = self.rng.choice(unique_ids, sample_size, replace=False)
        return df[df[self.id_col].isin(sample_ids)].copy()

    def _calc_sample_sizes(self):
        """Calculate sample sizes to simulate."""
        return (
            np.linspace(self.sample_min, self.sample_max, self.num_steps)
            .round()
            .astype(int)
        )

    def _generate_datasets(self):
        datasets = []
        for preprocessor in self.preprocessors:
            df_preproc = preprocessor(self.df)
            for sample_size in tqdm(self._calc_sample_sizes()):
                sample_func = (
                    self._sample_timestamps
                    if self.sample_timestamps
                    else self._sample_users
                )
                df_sample = sample_func(df_preproc, sample_size)
                for _ in range(self.num_runs):
                    df_assigned = self._create_treatment_assignments(df_sample)
                    for mdes in self.mdes:
                        df_effect = self._add_treatment_effect(
                            df_assigned, self.metric, mdes
                        )
                        datasets.append(
                            (df_effect, mdes, preprocessor.__name__, sample_size)
                        )
        return datasets

    def _experiment_eval(
        self,
        df: pd.DataFrame,
        mdes: float,
        preprocessor_name: str,
        sample_size: int,
        evaluator: callable,
        metric: str,
        alpha: float,
    ):
        p = evaluator(df, metric)
        is_statsig = p <= alpha
        result = ExperimentResult(
            preprocessor=preprocessor_name,
            evaluator=evaluator.__name__,
            sample_size=sample_size,
            mdes=mdes,
            power=is_statsig,
        )
        return result

    def run(self):
        print("Generating datasets...")
        datasets = self._generate_datasets()
        tasks = [
            (
                df,
                mdes,
                preprocessor_name,
                sample_size,
                evaluator,
                self.metric,
                self.alpha,
            )
            for df, mdes, preprocessor_name, sample_size in datasets
            for evaluator in self.evaluators
        ]

        print("Evaluating experiments...")
        results = [self._experiment_eval(*task) for task in tqdm(tasks)]

        result_cols = self._get_result_cols()
        result = Result(
            pd.DataFrame(results)
            .groupby(result_cols[:-1])
            .mean()
            .reset_index()
            .sort_values(result_cols)
        )
        return result
