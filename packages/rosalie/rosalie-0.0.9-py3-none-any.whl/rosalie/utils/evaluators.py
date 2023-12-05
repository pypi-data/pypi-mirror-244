import statsmodels.api as sm
from statsmodels.stats.weightstats import ttest_ind


def welch_t_test(df, metric):
    """Return p-value of Welch's t-test."""
    control_sample = df[df["assignments"] == "control"][metric]
    variant_sample = df[df["assignments"] == "treatment"][metric]
    _, p, _ = ttest_ind(control_sample, variant_sample, usevar="unequal")
    return p


def wls(df, metric):
    """Return p-value of weighted least squares regression."""
    y = df[metric]
    x = sm.add_constant(df["is_treated"].astype(float))
    w = df["assignments_freq"]
    model = sm.WLS(endog=y, exog=x, weights=w)
    results = model.fit()
    return results.pvalues["is_treated"]
