import nasdaqdatalink as quandl
import os
import pandas as pd
from datetime import date
from common import date_util


def get_prices(tickers, as_of_date, refresh=False):
    path = "/Users/weizhang/Documents/_GIT/quant-strategies/data/Sharadar/Prices/prices_" + as_of_date.strftime("%Y-%m-%d") + ".csv"
    if os.path.isfile(path) and (not refresh):
        return pd.read_csv(path)
    
    entry_price_df = quandl.get_table('SHARADAR/SEP', date=as_of_date.strftime("%Y-%m-%d"), ticker=tickers)
    exit_date = date_util.get_bus_month_end(as_of_date.year + (as_of_date.month + 1) // 13, as_of_date.month % 12 + 1)
    exit_price_df = quandl.get_table('SHARADAR/SEP', date=exit_date.strftime("%Y-%m-%d"), ticker=tickers)
    price_df = pd.merge(left=entry_price_df, right=exit_price_df, left_on="ticker", right_on="ticker", how="inner", suffixes=('', '_exit'))
    price_df["forward_return"] = price_df["closeadj_exit"] / price_df["closeadj"] - 1
    price_df.to_csv(path)
    
    return price_df


if __name__ == "__main__":
    quandl.ApiConfig.api_key = 'NRvcyMwNMXZ2ooDSM3nw'
    prices = get_prices(["MSFT"], date(2023, 8, 31))
    print(prices)