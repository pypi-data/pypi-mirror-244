def sample_min_max_specified(sample_min, sample_max):
    if (sample_max is None) ^ (sample_min is None):
        raise ValueError(
            "Both or neither of sample_max and sample_min must be specified."
        )


def sample_min_max_valid(sample_min, sample_max):
    if (sample_min and sample_max) and (sample_min > sample_max):
        raise ValueError("Min sample size cannot be larger than max sample size.")


def sample_min_max_size(
    df, time_col, id_col, sample_timestamps, sample_min, sample_max
):
    if (sample_timestamps and sample_max) and (df[time_col].nunique() < sample_max):
        raise ValueError(
            "Max sample size cannot be larger than number of time periods in the data."
        )

    if (not sample_timestamps and sample_max) and (df[id_col].nunique() < sample_max):
        raise ValueError(
            "Max sample size cannot be larger than number of units in the data."
        )


def evaluator_supplied(evaluators, baseline_evaluator):
    if (len(evaluators) == 0) and (baseline_evaluator is None):
        raise ValueError("At least one evaluator must be specified.")


def evaluator_names_unique(evaluators):
    if len(evaluators) != len(set(evaluators)):
        raise ValueError("Evaluator names must be unique.")


def preprocessor_names_unique(preprocessors):
    if len(preprocessors) != len(set(preprocessors)):
        raise ValueError("Preprocessor names must be unique.")
