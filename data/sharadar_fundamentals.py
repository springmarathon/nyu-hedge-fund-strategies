import nasdaqdatalink as quandl
import os
import pandas as pd
from datetime import date, timedelta


def get_fundamentals(tickers, as_of_date, refresh=False):
    path = "/Users/weizhang/Documents/_GIT/quant-strategies/data/Sharadar/Fundamentals/fundamentals_" + as_of_date.strftime("%Y-%m-%d") + ".csv"
    if os.path.isfile(path) and (not refresh):
        return pd.read_csv(path)
    
    start_date = as_of_date - timedelta(days=180)
    fundamentals = quandl.get_table('SHARADAR/SF1', datekey={'gte':start_date.strftime("%Y-%m-%d"), 'lte':as_of_date.strftime("%Y-%m-%d")}, dimension="ART", ticker=",".join(tickers))
    fundamentals = fundamentals.drop_duplicates("ticker", keep="first")
    
    fundamentals.to_csv(path)
    return fundamentals


if __name__ == "__main__":
    quandl.ApiConfig.api_key = 'NRvcyMwNMXZ2ooDSM3nw'
    fundamentals = get_fundamentals(["AAPL", "AMZN"], date(2004, 3, 31))