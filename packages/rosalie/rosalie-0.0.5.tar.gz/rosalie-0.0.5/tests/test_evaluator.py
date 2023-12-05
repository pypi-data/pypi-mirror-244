import pandas as pd
import pytest

from rosalie import Evaluator

# Sample test data
data = {
    "id": list(range(1, 101)),
    "y": list(range(100)),
    "timeframe": ["2021-01-01"] * 100,
}
df_sample = pd.DataFrame(data)


def test_create_treatment_assignments():
    evaluator = Evaluator(df_sample)
    df_assigned = evaluator._create_treatment_assignments(df_sample)

    # Ensure new columns were added
    assert "is_treated" in df_assigned.columns
    assert "assignments" in df_assigned.columns
    assert "assignments_freq" in df_assigned.columns

    # Ensure assignments are binary
    assert set(df_assigned["is_treated"].unique()) == {True, False}
    assert set(df_assigned["assignments"].unique()) == {"treatment", "control"}


def test_add_treatment_effect():
    evaluator = Evaluator(df_sample)
    df_assigned = evaluator._create_treatment_assignments(df_sample)
    df_effect = evaluator._add_treatment_effect(df_assigned, "y", 10)

    # Ensure the treatment group y values are increased by 10%
    treated = df_effect[df_effect["assignments"] == "treatment"]
    control = df_effect[df_effect["assignments"] == "control"]
    assert all(treated["y"] == control["y"] * 1.10)


@pytest.mark.parametrize("sample_size", [10, 50, 100])
def test_sample_users(sample_size):
    evaluator = Evaluator(df_sample)
    df_sampled = evaluator._sample_users(df_sample, sample_size)

    # Ensure sampled dataframe has the correct size
    assert len(df_sampled) == sample_size
