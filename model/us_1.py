import matplotlib.pyplot as plt
import nasdaqdatalink as quandl
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta
from common import date_util
from data import investment_universe, sharadar_fundamentals, sharadar_prices, sharadar_tickers
from signals import fundamental_signal


print(datetime.now())
quandl.ApiConfig.api_key = 'NRvcyMwNMXZ2ooDSM3nw'


dates = []
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

        if fundamentals.empty:
            continue
        dates.append(as_of_date)

        fundamentals = fundamental_signal.tangible_asset_to_price(fundamentals)
        fundamentals = fundamental_signal.ncf_to_ev(fundamentals)
        fundamentals = fundamental_signal.sales_to_price(fundamentals)

        fundamentals["tangible_asset_to_price_z"] = fundamentals.groupby("sector", group_keys=False)["tangible_asset_to_price"].apply(lambda x: (x - np.mean(x)) / np.std(x))
        fundamentals["ncf_to_ev_z"] = fundamentals.groupby("sector", group_keys=False)["ncf_to_ev"].apply(lambda x: (x - np.mean(x)) / np.std(x))
        fundamentals["sales_to_price_z"] = fundamentals.groupby("sector", group_keys=False)["sales_to_price"].apply(lambda x: (x - np.mean(x)) / np.std(x))

        fundamentals["composite"] = (fundamentals["tangible_asset_to_price_z"] + fundamentals["ncf_to_ev_z"] + fundamentals["sales_to_price_z"]) / 3

        fundamentals = fundamentals.sort_values("composite", ascending=False)
        fundamentals = fundamentals[~fundamentals["composite"].isna()]
        pnl.append(fundamentals[fundamentals["composite"] >= fundamentals.groupby("sector")["composite"].transform("quantile", 0.75)]["forward_return"].mean() - 
                   fundamentals[fundamentals["composite"] <= fundamentals.groupby("sector")["composite"].transform("quantile", 0.25)]["forward_return"].mean())

pnl = np.array(pnl)
file = open('/Users/weizhang/Documents/_GIT/quant-strategies/documents/us_1_{}.txt'.format(date.today().strftime("%Y-%m-%d")), 'w')
file.write("Annual Ret: {:.2%}\n".format(np.mean(pnl) * 12))
file.write("Annual Vol: {:.2%}\n".format(np.std(pnl) * np.sqrt(12)))
file.write("Sharpe Ratio: {:.2f}\n".format(np.mean(pnl) / np.std(pnl) * np.sqrt(12)))
cum_returns = np.cumprod(pnl + 1) - 1
high_watermark = np.maximum.accumulate(cum_returns)
drawdown = (high_watermark - cum_returns) / (1 + high_watermark)
file.write("Worst Drawdown: {:.2%}\n".format(np.max(drawdown)))

file.write("Percent Days Up: {:.2%}\n".format(len(pnl[pnl >= 0]) / len(pnl)))
file.write("Average Daily Gain: {:.2%}\n".format(np.mean(pnl[pnl >= 0])))
file.write("Average Daily Loss: {:.2%}\n".format(np.mean(pnl[pnl < 0])))
file.write("Best Month: {:.2%}\n".format(np.max(pnl)))
file.write("Worst Month: {:.2%}\n".format(np.min(pnl)))

file.write("1999 - 2009 Annual Ret: {:.2%}\n".format(np.mean(pnl[:120]) * 12))
file.write("1999 - 2009 Annual Vol: {:.2%}\n".format(np.std(pnl[:120]) * np.sqrt(12)))
file.write("1999 - 2009 Sharpe Ratio: {:.2f}\n".format(np.mean(pnl[:120]) / np.std(pnl[:120]) * np.sqrt(12)))

file.write("2009 - 2019 Annual Ret: {:.2%}\n".format(np.mean(pnl[120:]) * 12))
file.write("2009 - 2019 Annual Vol: {:.2%}\n".format(np.std(pnl[120:]) * np.sqrt(12)))
file.write("2009 - 2019 Sharpe Ratio: {:.2f}\n".format(np.mean(pnl[120:]) / np.std(pnl[120:]) * np.sqrt(12)))

file.close()
plt.plot(dates, np.cumprod(pnl + 1) - 1)
plt.savefig('/Users/weizhang/Documents/_GIT/quant-strategies/documents/us_1_{}.png'.format(date.today().strftime("%Y-%m-%d")))
print(datetime.now())