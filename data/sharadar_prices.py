import nasdaqdatalink as quandl
import os
import pandas as pd
from data import investment_universe
from datetime import date, timedelta
from common import date_util


def get_prices(tickers, as_of_date, refresh=False, update=False):
    path = "/Users/weizhang/Documents/_GIT/quant-strategies/data/Sharadar/Prices/prices_" + as_of_date.strftime("%Y-%m-%d") + ".csv"

    if os.path.isfile(path) and (not refresh):
        existing_price_df = pd.read_csv(path)
        existing_tickers = existing_price_df['ticker'].to_list()
        new_tickers = [x for x in tickers if x not in existing_tickers]
        if new_tickers and update:
            price_df = quandl.get_table('SHARADAR/SEP', date=as_of_date.strftime("%Y-%m-%d"), ticker=new_tickers)
            if not price_df.empty:
                existing_price_df = pd.concat([existing_price_df, price_df], ignore_index=True)
                existing_price_df.drop(columns=['Unnamed: 0'], inplace=True)
                existing_price_df.to_csv(path)
        return existing_price_df
    
    price_df = quandl.get_table('SHARADAR/SEP', date=as_of_date.strftime("%Y-%m-%d"), ticker=tickers)
    price_df.to_csv(path)
    
    return price_df


def get_90d_vol(tickers, as_of_date):
    path = "/Users/weizhang/Documents/_GIT/quant-strategies/data/Signals/Vol_90D/signal_" + as_of_date.strftime("%Y-%m-%d") + ".csv"
    if os.path.isfile(path):
        existing_signal_df = pd.read_csv(path)
        existing_signal_df.set_index("ticker", inplace=True)
        return existing_signal_df
    price_df = quandl.get_table('SHARADAR/SEP', date={'gte':(as_of_date - timedelta(weeks=13)).strftime("%Y-%m-%d"), 'lte':as_of_date.strftime("%Y-%m-%d")}, ticker=tickers, paginate=True)
    signal_df = pd.DataFrame(price_df.pivot(index='date', columns='ticker', values='closeadj').pct_change().tail(-1).std(axis=0))
    signal_df.columns = ["Vol_90D"]
    signal_df.to_csv(path)
    return signal_df


if __name__ == "__main__":
    quandl.ApiConfig.api_key = 'NRvcyMwNMXZ2ooDSM3nw'
    universe = investment_universe.get_SPX(date(2021, 12, 8), refresh=True)
    # signal_df = get_90d_vol(universe['ticker'].to_list(), date(2023, 9, 30))
    prices = get_prices(universe['ticker'].to_list(), date(2021, 12, 8), date_util.get_next_rebal_day(date(2021, 12, 8), 3), refresh=True, update=True)
    # print(prices)
    print("Hello World")