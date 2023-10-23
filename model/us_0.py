import nasdaqdatalink as quandl
import numpy as np
import pandas as pd
from datetime import datetime
from common import date_util
from data import investment_universe, sharadar_fundamentals, sharadar_prices, sharadar_tickers
from signals import fundamental_signal


print(datetime.now())
quandl.ApiConfig.api_key = 'NRvcyMwNMXZ2ooDSM3nw'


pnl = []
for i in range(1999, 2020):
    for j in range(1, 13):
        as_of_date = date_util.get_bus_month_end(i, j)
        universe = investment_universe.get_SPX(as_of_date)
        fundamentals = sharadar_fundamentals.get_fundamentals(universe['ticker'].to_list(), as_of_date)
        prices = sharadar_prices.get_prices(universe['ticker'].to_list(), as_of_date)
        price_df = prices[["ticker", "forward_return"]]
        sectors = sharadar_tickers.get_tickers(universe['ticker'].to_list(), as_of_date)
        sectors = sectors[["ticker", "sector"]]
        fundamentals = pd.merge(fundamentals, sectors, left_on="ticker", right_on="ticker", how="inner")
        fundamentals = pd.merge(fundamentals, price_df, left_on="ticker", right_on="ticker", how="inner")

        fundamentals = fundamental_signal.operating_leverage(fundamentals)
        fundamentals = fundamental_signal.gross_margin(fundamentals)
        fundamentals = fundamental_signal.return_on_equity(fundamentals)
        fundamentals = fundamental_signal.dividend_yield(fundamentals)
        fundamentals = fundamental_signal.earnings_to_price(fundamentals)
        fundamentals = fundamental_signal.ofcf_to_ev(fundamentals)
        fundamentals = fundamental_signal.tangible_book_to_price(fundamentals)

        fundamentals["operating_leverage_z"] = fundamentals.groupby("sector", group_keys=False)["operating_leverage"].apply(lambda x: (x - np.mean(x)) / np.std(x))
        fundamentals["return_on_equity_z"] = fundamentals.groupby("sector", group_keys=False)["return_on_equity"].apply(lambda x: (x - np.mean(x)) / np.std(x))
        fundamentals["gross_margin_z"] = fundamentals.groupby("sector", group_keys=False)["gross_margin"].apply(lambda x: (x - np.mean(x)) / np.std(x))
        fundamentals["quality"] = (fundamentals["operating_leverage_z"] + fundamentals["return_on_equity_z"] + fundamentals["gross_margin_z"]) / 3

        fundamentals["dividend_yield_z"] = fundamentals.groupby("sector", group_keys=False)["dividend_yield"].apply(lambda x: (x - np.mean(x)) / np.std(x))
        fundamentals["earnings_to_price_z"] = fundamentals.groupby("sector", group_keys=False)["earnings_to_price"].apply(lambda x: (x - np.mean(x)) / np.std(x))
        fundamentals["ofcf_to_ev_z"] = fundamentals.groupby("sector", group_keys=False)["ofcf_to_ev"].apply(lambda x: (x - np.mean(x)) / np.std(x))
        fundamentals["tangible_book_to_price_z"] = fundamentals.groupby("sector", group_keys=False)["tangible_book_to_price"].apply(lambda x: (x - np.mean(x)) / np.std(x))
        fundamentals["value"] = (fundamentals["dividend_yield_z"] + fundamentals["earnings_to_price_z"] + fundamentals["ofcf_to_ev_z"] + fundamentals["tangible_book_to_price_z"]) / 4

        fundamentals["composite"] = (fundamentals["quality"] + fundamentals["value"]) / 2

        fundamentals = fundamentals.sort_values("composite", ascending=False)
        fundamentals = fundamentals[~fundamentals["composite"].isna()]
        pnl.append(fundamentals[fundamentals["composite"] >= fundamentals.groupby("sector")["composite"].transform("quantile", 0.8)]["forward_return"].mean() - 
                   fundamentals[fundamentals["composite"] <= fundamentals.groupby("sector")["composite"].transform("quantile", 0.2)]["forward_return"].mean())
        
print(sum(pnl))
print(np.mean(pnl) / np.std(pnl) * np.sqrt(12))
print(datetime.now())