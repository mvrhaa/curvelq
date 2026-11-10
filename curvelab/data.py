import os
import io
import pandas as pd
import requests
from curvelab import config

URL = "https://data-api.ecb.europa.eu/service/data/YC/B.U2.EUR.4F.G_N_A.SV_C_YM."

def download_series(code):
    params = {
        "format":"csvdata",
        "startPeriod": config.START_DATE,
        "endPeriod": config.END_DATE,
    }
    response = requests.get(URL + code, params = params )
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text))
    df = df[["TIME_PERIOD","OBS_VALUE"]]
    df.columns = ["date","rate"]
    df["date"] = pd.to_datetime(df["date"])
    return df

def download_all():
    columns = {}
    for maturity,code in config.ECB_CODES.items():
        df = download_series(code)
        columns[maturity] = df.set_index("date")["rate"]
    table = pd.concat(columns, axis=1)
    os.makedirs("data/raw", exist_ok=True)
    table.to_csv("data/raw/yields.csv")
    return table