import os
import sys

from curvelab import compare, data, holdout, ns_params, plots, summary


def run(refresh):
    os.makedirs("outputs", exist_ok=True)

    print("1/6 data")
    table = data.load_yields(refresh=refresh)
    data.check_data(table)
    table = data.clean_data(table)

    print("2/6 plots")
    plots.plot_curves(table)
    plots.plot_10y(table)
    plots.plot_linear_vs_spline(table, "2023-06-30")

    print("3/6 Nelson-Siegel parameters")
    params = ns_params.fit_all_days(table)
    params.to_csv("outputs/ns_params.csv")
    plots.plot_ns_params(params)

    print("4/6 holdout")
    errors = holdout.run_holdout(table)
    errors.to_csv("outputs/holdout_errors.csv", index=False)

    print("5/6 summary")
    text = summary.make_summary(errors)
    open("outputs/summary.md", "w").write(text)
    plots.plot_holdout_errors(errors)
    print(text)

    print("6/6 bond prices")
    prices = compare.price_all_days(table)
    prices.to_csv("outputs/bond_prices.csv", index=False)
    text = compare.make_comparison(prices)
    open("outputs/bond_comparison.md", "w").write(text)
    print(text)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run(refresh="--refresh" in sys.argv)
    else:
        print("usage: python -m curvelab run [--refresh]")
