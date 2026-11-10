import numpy as np
import pandas as pd

from curvelab.plots import plot_holdout_errors


def rmse(errors):
    """Root mean squared error."""
    return np.sqrt((errors ** 2).mean())


def to_markdown(table, first_column):
    """Turn a table into markdown text."""
    lines = ["| " + first_column + " | " + " | ".join(str(c) for c in table.columns) + " |"]
    lines.append("|---" * (len(table.columns) + 1) + "|")
    for name, row in table.iterrows():
        lines.append("| " + str(name) + " | " + " | ".join("%.2f" % v for v in row) + " |")
    return "\n".join(lines)


def make_summary(errors):
    """RMSE in bp by method, by maturity and by year, as markdown text."""
    by_method = errors.groupby("method")["error_bp"].apply(rmse).to_frame("RMSE, bp")
    by_maturity = errors.groupby(["method", "maturity"])["error_bp"].apply(rmse).unstack()
    by_maturity.columns = ["%gY" % m for m in by_maturity.columns]
    years = errors["date"].dt.year
    by_year = errors.groupby([years, "method"])["error_bp"].apply(rmse).unstack()
    text = "# Holdout RMSE in bp\n\n"
    text += "Hidden maturities: 2Y, 7Y, 15Y. Curves are built from the other 8 maturities.\n\n"
    text += "## By method\n\n" + to_markdown(by_method, "method") + "\n\n"
    text += "## By method and maturity\n\n" + to_markdown(by_maturity, "method") + "\n\n"
    text += "## By year\n\n" + to_markdown(by_year, "year") + "\n"
    return text


if __name__ == "__main__":
    errors = pd.read_csv("outputs/holdout_errors.csv", parse_dates=["date"])
    text = make_summary(errors)
    open("outputs/summary.md", "w").write(text)
    print(text)
    plot_holdout_errors(errors)
