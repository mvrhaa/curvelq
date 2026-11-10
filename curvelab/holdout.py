import os

import pandas as pd

from curvelab.curves import LinearCurve, NelsonSiegelCurve, SplineCurve
from curvelab.data import load_clean

HIDDEN = [2, 7, 15]
METHODS = {
    "linear": LinearCurve,
    "spline": SplineCurve,
    "nelson_siegel": NelsonSiegelCurve,
}


def split_maturities(maturities, hidden=HIDDEN):
    known = [m for m in maturities if m not in hidden]
    hidden = [m for m in maturities if m in hidden]
    return known, hidden


def holdout_error(curve, row, hidden=HIDDEN):
    known, hidden = split_maturities(row.index, hidden)
    curve.fit(known, row[known].values)
    errors = (curve.rate(hidden) - row[hidden].values) * 100
    return pd.Series(errors, index=hidden)


def run_holdout(table):
    rows = []
    for date, row in table.iterrows():
        for name, method in METHODS.items():
            errors = holdout_error(method(), row)
            for maturity, error in errors.items():
                rows.append([date, name, maturity, error])
    return pd.DataFrame(rows, columns=["date", "method", "maturity", "error_bp"])


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    table = load_clean()
    errors = run_holdout(table)
    errors.to_csv("outputs/holdout_errors.csv", index=False)
    print(errors.shape)
    print(errors.head(9))
