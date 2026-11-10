import os

import pandas as pd

from curvelab.data import load_clean
from curvelab.holdout import METHODS
from curvelab.pricing import price_bond
from curvelab.summary import to_markdown

COUPON = 3.0
BONDS = [10, 30]


def price_all_days(table):
    rows = []
    for date, row in table.iterrows():
        curves = {}
        for name, method in METHODS.items():
            curves[name] = method().fit(row.index, row.values)
        for years in BONDS:
            prices = [price_bond(curves[name], COUPON, years) for name in METHODS]
            rows.append([date, years] + prices)
    return pd.DataFrame(rows, columns=["date", "years"] + list(METHODS))


def compare_to_spline(prices):
    rows = {}
    for years in BONDS:
        bond = prices[prices["years"] == years]
        for name in ["linear", "nelson_siegel"]:
            diff = (bond[name] - bond["spline"]).abs()
            rows["%dY bond, %s vs spline" % (years, name)] = [diff.mean(), diff.max()]
    return pd.DataFrame(rows, index=["mean abs difference", "max abs difference"]).T


def make_comparison(prices):
    text = "# Bond price by curve method\n\n"
    text += "Bond: coupon 3%, annual, nominal 100. Curves are built from all 11 maturities. "
    text += "Differences are in price points (1.00 = 1% of nominal).\n\n"
    text += to_markdown(compare_to_spline(prices), "comparison") + "\n"
    return text


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    table = load_clean()
    prices = price_all_days(table)
    prices.to_csv("outputs/bond_prices.csv", index=False)
    text = make_comparison(prices)
    open("outputs/bond_comparison.md", "w").write(text)
    print(text)
