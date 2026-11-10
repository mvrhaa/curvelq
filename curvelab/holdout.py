import pandas as pd

HIDDEN = [2, 7, 15]


def split_maturities(maturities, hidden=HIDDEN):
    known = [m for m in maturities if m not in hidden]
    hidden = [m for m in maturities if m in hidden]
    return known, hidden


def holdout_error(curve, row, hidden=HIDDEN):
    known, hidden = split_maturities(row.index, hidden)
    curve.fit(known, row[known].values)
    errors = (curve.rate(hidden) - row[hidden].values) * 100
    return pd.Series(errors, index=hidden)
