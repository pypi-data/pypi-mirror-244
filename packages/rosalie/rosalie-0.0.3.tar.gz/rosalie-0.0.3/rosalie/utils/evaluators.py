import statsmodels.api as sm


def wls(df, metric):
    y = df[metric]
    x = sm.add_constant(df["is_treated"].astype(float))
    w = df["assignments_freq"]
    model = sm.WLS(endog=y, exog=x, weights=w)
    results = model.fit()
    return results.pvalues["is_treated"]
