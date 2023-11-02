import matplotlib.pyplot as plt
import nasdaqdatalink as quandl
import numpy as np
import pandas as pd
from scipy import stats
from datetime import date, datetime, timedelta
from common import date_util, math_util
from data import investment_universe, sharadar_fundamentals, sharadar_prices, sharadar_tickers
from signals import fundamental_signal


print(datetime.now())
quandl.ApiConfig.api_key = 'NRvcyMwNMXZ2ooDSM3nw'


dates = []
pnl = []
rebal_date = date(1999, 1, 1)
while rebal_date <= date(2020, 12, 31):
    rebal_date = date_util.get_next_rebal_day(rebal_date, 3)

    dates.append(rebal_date)
    universe = investment_universe.get_SPX(rebal_date)
    fundamentals = sharadar_fundamentals.get_fundamentals(universe['ticker'].to_list(), rebal_date)
    p_fundamentals = sharadar_fundamentals.get_fundamentals(universe['ticker'].to_list(), rebal_date - timedelta(weeks=52))
    prices = sharadar_prices.get_prices(universe['ticker'].to_list(), rebal_date, date_util.get_next_rebal_day(rebal_date, 3))
    price_df = prices[["ticker", "closeadj", "forward_return"]]
    sectors = sharadar_tickers.get_tickers(universe['ticker'].to_list(), rebal_date)
    sectors = sectors[["ticker", "sector"]]
    fundamentals = pd.merge(fundamentals, sectors, left_on="ticker", right_on="ticker", how="inner")
    fundamentals = pd.merge(fundamentals, price_df, left_on="ticker", right_on="ticker", how="inner")
    fundamentals = pd.merge(fundamentals, p_fundamentals, left_on="ticker", right_on="ticker", how="inner", suffixes=["", "_1y"])

    fundamentals = fundamental_signal.tangible_asset_to_price(fundamentals)
    fundamentals = fundamental_signal.ncf_to_ev(fundamentals)
    fundamentals = fundamental_signal.sales_to_price(fundamentals)
    fundamentals = fundamental_signal.accruals(fundamentals)
    fundamentals = fundamental_signal.fcf_to_ic_growth(fundamentals)

    fundamentals = math_util.normalize(fundamentals, "tangible_asset_to_price")
    fundamentals = math_util.normalize(fundamentals, "ncf_to_ev")
    fundamentals = math_util.normalize(fundamentals, "sales_to_price")
    fundamentals = math_util.normalize(fundamentals, "accruals")
    fundamentals = math_util.normalize(fundamentals, "fcf_to_ic_growth")

    # previous_month = date_util.get_previous_month_end(rebal_date)
    # previous_month_df = sharadar_prices.get_prices(universe['ticker'].to_list(), previous_month)
    # previous_month_df = previous_month_df[["ticker", "closeadj"]]

    # previous_year = date_util.get_bus_month_end(rebal_date.year - 1, rebal_date.month)
    # previous_year_df = sharadar_prices.get_prices(universe['ticker'].to_list(), previous_year)
    # previous_year_df = previous_year_df[["ticker", "closeadj"]]

    # fundamentals = pd.merge(fundamentals, previous_month_df, left_on="ticker", right_on="ticker", how="inner", suffixes=["", "_1m"])
    # fundamentals = pd.merge(fundamentals, previous_year_df, left_on="ticker", right_on="ticker", how="inner", suffixes=["", "_1y"])

    # fundamentals["momentum"] = fundamentals["closeadj_1m"] / fundamentals["closeadj_1y"] - 1
    # fundamentals["momentum_z"] = fundamentals.groupby("sector", group_keys=False)["momentum"].apply(lambda x: (x - np.mean(x)) / np.std(x))

    fundamentals["composite"] = (fundamentals["tangible_asset_to_price_z"] + fundamentals["ncf_to_ev_z"] + fundamentals["sales_to_price_z"] + fundamentals["accruals_z"] + fundamentals["fcf_to_ic_growth_z"]) / 5

    fundamentals = fundamentals.sort_values("composite", ascending=False)
    fundamentals = fundamentals[~fundamentals["composite"].isna()]
    pnl.append(fundamentals[fundamentals["composite"] >= fundamentals.groupby("sector")["composite"].transform("quantile", 0.75)]["forward_return"].mean() - 
                fundamentals[fundamentals["composite"] <= fundamentals.groupby("sector")["composite"].transform("quantile", 0.25)]["forward_return"].mean())

pnl = np.array(pnl)
pnl[np.isnan(pnl)] = 0

pnl_df = pd.DataFrame({"date": dates, "return": pnl})
pnl_df["date"] = pd.to_datetime(pnl_df["date"])
pnl_df.set_index("date", inplace=True)

file = open('/Users/weizhang/Documents/_GIT/quant-strategies/documents/us_2_{}.txt'.format(date.today().strftime("%Y-%m-%d")), 'w')

file.write("Full Sample:\n")
file.write("Annual Ret: {:.2%}\n".format(np.mean(pnl) * 52))
file.write("Annual Vol: {:.2%}\n".format(np.std(pnl) * np.sqrt(52)))
file.write("Sharpe Ratio: {:.2f}\n".format(np.mean(pnl) / np.std(pnl) * np.sqrt(52)))
file.write("t-Statistic: {:.2f}\n".format(stats.ttest_1samp(pnl, popmean=0).statistic))
cum_returns = np.cumprod(pnl + 1) - 1
high_watermark = np.maximum.accumulate(cum_returns)
drawdown = high_watermark - cum_returns
file.write("Worst Drawdown: {:.2%}\n".format(np.max(drawdown)))
file.write("Percent Weeks Up: {:.2%}\n".format(len(pnl[pnl >= 0]) / len(pnl)))
file.write("Average Weekly Gain: {:.2%}\n".format(np.mean(pnl[pnl >= 0])))
file.write("Average Weekly Loss: {:.2%}\n".format(np.mean(pnl[pnl < 0])))
file.write("Best Week: {:.2%}\n".format(np.max(pnl)))
file.write("Worst Week: {:.2%}\n".format(np.min(pnl)))

file.write("1999 - 2008 Annual Ret: {:.2%}\n".format(np.mean(pnl_df.loc["1999":"2008", "return"]) * 52))
file.write("1999 - 2008 Annual Vol: {:.2%}\n".format(np.std(pnl_df.loc["1999":"2008", "return"]) * np.sqrt(52)))
file.write("1999 - 2008 Sharpe Ratio: {:.2f}\n".format(np.mean(pnl_df.loc["1999":"2008", "return"]) / np.std(pnl_df.loc["1999":"2008", "return"]) * np.sqrt(52)))

file.write("2009 - 2018 Annual Ret: {:.2%}\n".format(np.mean(pnl_df.loc["2009":"2018", "return"]) * 52))
file.write("2009 - 2018 Annual Vol: {:.2%}\n".format(np.std(pnl_df.loc["2009":"2018", "return"]) * np.sqrt(52)))
file.write("2009 - 2018 Sharpe Ratio: {:.2f}\n".format(np.mean(pnl_df.loc["2009":"2018", "return"]) / np.std(pnl_df.loc["2009":"2018", "return"]) * np.sqrt(52)))

file.write("2019 - 2020 Annual Ret: {:.2%}\n".format(np.mean(pnl_df.loc["2019":"2020", "return"]) * 52))
file.write("2019 - 2020 Annual Vol: {:.2%}\n".format(np.std(pnl_df.loc["2019":"2020", "return"]) * np.sqrt(52)))
file.write("2019 - 2020 Sharpe Ratio: {:.2f}\n".format(np.mean(pnl_df.loc["2019":"2020", "return"]) / np.std(pnl_df.loc["2019":"2020", "return"]) * np.sqrt(52)))

file.write(pnl_df.groupby(pnl_df.index.year).sum().to_string())
file.close()

plt.ioff()
plt.plot(dates, np.cumprod(pnl + 1) - 1)
plt.savefig('/Users/weizhang/Documents/_GIT/quant-strategies/documents/us_2_{}.png'.format(date.today().strftime("%Y-%m-%d")))

pnl_df.to_csv('/Users/weizhang/Documents/_GIT/quant-strategies/documents/us_2_{}.csv'.format(date.today().strftime("%Y-%m-%d")), index=False)

print(datetime.now())