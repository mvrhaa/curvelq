import os

import pandas as pd

from curvelab.curves import NelsonSiegelCurve
from curvelab.data import load_clean
from curvelab.plots import plot_ns_params


def fit_all_days(table):
    """Fit Nelson-Siegel on every day. Returns a table with b0, b1, b2 and lambda by date."""
    rows = []
    for date, row in table.iterrows():
        curve = NelsonSiegelCurve().fit(row.index, row.values)
        rows.append([date, curve.betas[0], curve.betas[1], curve.betas[2], curve.lam])
    params = pd.DataFrame(rows, columns=["date", "b0", "b1", "b2", "lam"])
    params = params.set_index("date")
    return params


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    table = load_clean()
    params = fit_all_days(table)
    params.to_csv("outputs/ns_params.csv")
    print(params.resample("YE").mean().round(2))
    plot_ns_params(params)
