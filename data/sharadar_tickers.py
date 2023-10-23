import nasdaqdatalink as quandl
import os
import pandas as pd
from datetime import date


def get_tickers(tickers, as_of_date, refresh=False):
    path = "/Users/weizhang/Documents/_GIT/quant-strategies/data/Sharadar/Tickers/tickers_" + as_of_date.strftime("%Y-%m-%d") + ".csv"
    if os.path.isfile(path) and (not refresh):
        return pd.read_csv(path)

    sectors = quandl.get_table('SHARADAR/TICKERS', table='SF1', ticker=tickers)        
    sectors.to_csv(path)
    return sectors


if __name__ == "__main__":
    quandl.ApiConfig.api_key = 'NRvcyMwNMXZ2ooDSM3nw'
    fundamentals = get_tickers(["AAPL", "AMZN"], date(2004, 3, 31))