import os
import matplotlib.pyplot as plt
from curvelab.data import load_clean

DATES = ["2019-06-28","2020-08-31","2022-06-30","2023-06-30"]

def plot_curves(table):
    plt.figure(figsize=(8,5))
    for date in DATES:
        row = table.loc[:date].iloc[-1]
        plt.plot(row.index,row.values,marker="o",label=date)
        plt.axhline(0,color="gray",linewidth=0.8)
        plt.xlabel("Maturity,years")
        plt.ylabel("Spot rate,%")
        plt.title("Euro area AAA yield curve")
        plt.legend()
        plt.savefig("outputs/curves.png",dpi=150)
        plt.close()

def plot_10y(table):
    plt.figure(figsize=(8,5))
    plt.plot(table.index,table[10])
    plt.axhline(0,color="gray",linewidth=0.8)
    plt.xlabel("Date")
    plt.ylabel("10Y spot rate,%")
    plt.title("Euro area AAA 10Y yield")
    plt.savefig("outputs/history_10y.png",dpi=150)
    plt.close()

if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    table = load_clean()
    plot_curves(table)
    plot_10y(table)
