import os

import matplotlib.pyplot as plt
import numpy as np

from curvelab.curves import LinearCurve, SplineCurve
from curvelab.data import load_clean

DATES = ["2019-06-28", "2020-08-31", "2022-06-30", "2023-06-30"]


def plot_curves(table):
    plt.figure(figsize=(8, 5))
    for date in DATES:
        row = table.loc[:date].iloc[-1]
        plt.plot(row.index, row.values, marker="o", label=date)
    plt.axhline(0, color="gray", linewidth=0.8)
    plt.xlabel("Maturity, years")
    plt.ylabel("Spot rate, %")
    plt.title("Euro area AAA yield curve")
    plt.legend()
    plt.savefig("outputs/curves.png", dpi=150)
    plt.close()


def plot_10y(table):
    plt.figure(figsize=(8, 5))
    plt.plot(table.index, table[10.0])
    plt.axhline(0, color="gray", linewidth=0.8)
    plt.xlabel("Date")
    plt.ylabel("10Y spot rate, %")
    plt.title("Euro area AAA 10Y spot rate")
    plt.savefig("outputs/history_10y.png", dpi=150)
    plt.close()


def plot_linear_vs_spline(table, date):
    row = table.loc[:date].iloc[-1]
    grid = np.linspace(0.25, 30, 300)
    linear = LinearCurve().fit(row.index, row.values)
    spline = SplineCurve().fit(row.index, row.values)
    plt.figure(figsize=(8, 5))
    plt.plot(grid, linear.rate(grid), label="linear")
    plt.plot(grid, spline.rate(grid), label="spline")
    plt.scatter(row.index, row.values, color="black", zorder=3, label="ECB points")
    plt.xlabel("Maturity, years")
    plt.ylabel("Spot rate, %")
    plt.title("Linear vs spline, " + date)
    plt.legend()
    plt.savefig("outputs/linear_vs_spline.png", dpi=150)
    plt.close()


def plot_ns_params(params):
    plt.figure(figsize=(8, 5))
    plt.plot(params.index, params["b0"], label="b0 level")
    plt.plot(params.index, params["b1"], label="b1 slope")
    plt.plot(params.index, params["b2"], label="b2 curvature")
    plt.axhline(0, color="gray", linewidth=0.8)
    plt.xlabel("Date")
    plt.ylabel("Value, %")
    plt.title("Nelson-Siegel parameters over time")
    plt.legend()
    plt.savefig("outputs/ns_params.png", dpi=150)
    plt.close()


def plot_holdout_errors(errors):
    months = errors["date"].dt.to_period("M").dt.to_timestamp()
    squared = errors["error_bp"] ** 2
    monthly = np.sqrt(squared.groupby([months, errors["method"]]).mean()).unstack()
    plt.figure(figsize=(8, 5))
    for method in monthly.columns:
        plt.plot(monthly.index, monthly[method], label=method)
    plt.xlabel("Date")
    plt.ylabel("Monthly holdout RMSE, bp")
    plt.title("Holdout error over time (hidden 2Y, 7Y, 15Y)")
    plt.legend()
    plt.savefig("outputs/holdout_errors.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    table = load_clean()
    plot_curves(table)
    plot_10y(table)
    plot_linear_vs_spline(table, "2023-06-30")
