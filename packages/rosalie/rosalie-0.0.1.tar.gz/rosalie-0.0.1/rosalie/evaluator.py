import dataclasses
from collections import defaultdict, namedtuple
from copy import copy
from dataclasses import dataclass

import numpy as np
import pandas as pd
from statsmodels.stats.weightstats import ttest_ind
from tqdm import tqdm


@dataclass
class Evaluator:
    df: pd.DataFrame
    preprocessors: list = dataclasses.field(default_factory=list)
    evaluators: list = dataclasses.field(default_factory=list)
    sample_min: int = 100_000
    sample_max: int = 200_000
    step_size: int = 10_000
    mdes: float = 1
    num_runs: int = 100
    sample_timestamps: bool = False
    alpha: float = 0.05
    metric: str = "y"
    random_seed: int = 2312
    use_default_preprocessor: bool = False
    use_default_evaluator: bool = False
    id_col: str = ("id",)
    testing: bool = (False,)
    """
    Class to simulate experiments.
    
    Arguments:
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

    def __post_init__(self):
        # Instantiate random number generator
        self.rng = np.random.default_rng(self.random_seed)

        # Add default callables
        if self.use_default_preprocessor:
            self.preprocessors = copy(self.preprocessors)
            self.preprocessors.insert(0, self.default_preprocessor)

        if self.use_default_evaluator:
            self.evaluators = copy(self.evaluators)
            self.evaluators.insert(0, self.default_evaluator)

        # Perform input checks
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

        assert (
            len(self.preprocessors) > 0
        ), "At least one preprocessor must be specified."
        assert len(self.evaluators) > 0, "At least one evaluator must be specified."
        assert (
            self.sample_min <= self.sample_max
        ), "Min sample size cannot be larger than max sample size."

    def default_preprocessor(self, df):
        """Return unprocessed data."""
        return df

    def default_evaluator(self, df, metric):
        """Return p-value of Welch's t-test (not assuming equal variance)."""
        control_sample = df[df["assignments"] == "control"][metric]
        variant_sample = df[df["assignments"] == "treatment"][metric]
        t, p, df = ttest_ind(control_sample, variant_sample, usevar="unequal")
        return p

    def _create_treatment_assignments(self, df):
        """Add columns with treatment assignments to dataframe."""
        g = df.groupby(self.id_col)
        assign = lambda x: self.rng.choice([True, False])
        labels = {True: "treatment", False: "control"}
        df["is_treated"] = None
        df["is_treated"] = g["is_treated"].transform(assign)
        df["assignments"] = df["is_treated"].map(labels)
        df["assignments_freq"] = 1
        return df

    def _add_treatment_effect(self, df):
        """Add column with artificial treatment effect to dataframe."""
        map = {"control": 1.0, "treatment": (1 + self.mdes / 100)}
        multiplier = df["assignments"].map(map)
        df[self.metric] = df[self.metric] * multiplier
        return df

    def _sample_timestamps(self, df, sample_size):
        """Sample timestamps from dataframe."""
        unique_timestamps = sorted(df["timeframe"].unique())
        sample_timestamps = unique_timestamps[:sample_size]
        return df[df["timeframe"].isin(sample_timestamps)]

    def _sample_users(self, df, sample_size):
        """Sample users from dataframe."""
        unique_ids = df[self.id_col].unique()
        sample_ids = self.rng.choice(unique_ids, sample_size, replace=False)
        return df[df[self.id_col].isin(sample_ids)]

    def simulate(self):
        """Simulate experiment and return results as a dataframe.

        Note on sampling:
        If samples are drawn once for each sample size, experiment results are
        based on randomisation variation only. If samples are drawn separately
        for each run, experiment results are based on both randomisation
        variation and sampling variation. For large samples, drawing a single
        sample (ignoring sampling variation) will make little difference to the
        results (the variation among large samples is low), but significantly
        improves performance of the simulation engine, which is why we do it.
        """
        ExperimentResult = namedtuple(
            "ExperimentResult", ["preprocessor", "evaluator", "sample_size", "power"]
        )
        sample_sizes = range(self.sample_min, self.sample_max + 1, self.step_size)

        results = []
        for preprocessor in self.preprocessors:
            df_preproc = preprocessor(self.df)

            for sample_size in tqdm(sample_sizes):
                if self.sample_timestamps:
                    df_sample = self._sample_timestamps(df_preproc, sample_size)
                else:
                    df_sample = self._sample_users(df_preproc, sample_size)

                sample_results = defaultdict(list)
                for _ in range(self.num_runs):
                    df_sample = self._create_treatment_assignments(df_sample)
                    df_sample = self._add_treatment_effect(df_sample)
                    for evaluator in self.evaluators:
                        p = evaluator(df_sample, self.metric)
                        is_statsig = p <= self.alpha
                        sample_results[evaluator.__name__].append(is_statsig)
                        if self.testing:
                            print(evaluator, p)

                for evaluator in sample_results:
                    power = np.mean(sample_results[evaluator])
                    result = ExperimentResult(
                        preprocessor=preprocessor.__name__,
                        evaluator=evaluator,
                        sample_size=sample_size,
                        power=power,
                    )
                    results.append(result)

        return pd.DataFrame(results).sort_values(result_cols)
