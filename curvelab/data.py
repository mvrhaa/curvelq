import time
import sys
import os
import io
import pandas as pd
import requests
from curvelab import config

URL = "https://data-api.ecb.europa.eu/service/data/YC/B.U2.EUR.4F.G_N_A.SV_C_YM."
PATH = "data/raw/yields.csv"
CLEAN_PATH = "data/clean/yields.csv"

def download_series(code):
    """Download one maturity from the ECB API. Returns a table with date and rate in percent."""
    params = {
        "format":"csvdata",
        "startPeriod": config.START_DATE,
        "endPeriod": config.END_DATE,
    }
    for attempt in range(5):
        response = requests.get(URL + code, params=params)
        if response.status_code == 200:
            break
        print("retry", code, response.status_code)
        time.sleep(5)
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text))
    df = df[["TIME_PERIOD","OBS_VALUE"]]
    df.columns = ["date","rate"]
    df["date"] = pd.to_datetime(df["date"])
    return df

def download_all():
    """Download all maturities and merge them into one table: rows are dates, columns are maturities in years."""
    columns = {}
    for maturity,code in config.ECB_CODES.items():
        df = download_series(code)
        columns[maturity] = df.set_index("date")["rate"]
    table = pd.concat(columns, axis=1)
    os.makedirs("data/raw", exist_ok=True)
    table.to_csv(PATH)
    return table

def load_yields(refresh=False):
    """Read the raw table from the CSV cache, or download it if there is no cache or refresh is asked."""
    if os.path.exists(PATH) and not refresh:
        print("reading from cache")
        table = pd.read_csv(PATH, index_col="date", parse_dates=True)
        table.columns = table.columns.astype(float)
        return table
    print("downloading from ECB")
    return download_all()

def check_data(table):
    """Print a short report: missing values, incomplete days and daily jumps above 50 bp."""
    print("days",len(table))
    print("missing values per maturity:")
    print(table.isna().sum())
    print("days with missing maturities:",table.isna().any(axis=1).sum())
    jumps = table.diff().abs()>0.5
    print("jumps over 50 bp per maturity:")
    print(jumps.sum())
    print("dates with jumps:")
    print(table.index[jumps.any(axis=1)].tolist())

def clean_data(table):
    """Drop days with missing values and save the clean table."""
    clean = table.dropna()
    os.makedirs("data/clean", exist_ok=True)
    clean.to_csv(CLEAN_PATH)
    print("days before:", len(table), "days after:", len(clean))
    return clean


def load_clean():
    """Read the clean table saved by clean_data."""
    table = pd.read_csv(CLEAN_PATH, index_col="date", parse_dates=True)
    table.columns = table.columns.astype(float)
    return table

if __name__ == "__main__":
    table = load_yields(refresh="--refresh" in sys.argv)
    print(table.shape)
    check_data(table)
    clean_data(table)
