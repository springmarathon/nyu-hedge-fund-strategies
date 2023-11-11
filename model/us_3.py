import matplotlib.pyplot as plt
import nasdaqdatalink as quandl
import numpy as np
import os
import pandas as pd
from scipy import stats
from datetime import date, datetime, timedelta
from common import date_util, math_util
from data import investment_universe, sharadar_fundamentals, sharadar_prices, sharadar_tickers
from signals import fundamental_signal


quandl.ApiConfig.api_key = 'NRvcyMwNMXZ2ooDSM3nw'
model_name = "us_3"
home_path = "/Users/weizhang/Documents/_GIT/quant-strategies"

file = open(home_path + '/documents/' + model_name + '_{}.txt'.format(date.today().strftime("%Y-%m-%d")), 'w')
file.write("Run start time: {:%d/%m/%y %H:%M:%S}\n".format(datetime.now()))


def get_data(rebal_date, refresh=False):
    path = home_path + "/data/Signals/Combined/" + model_name + "/signals_" + rebal_date.strftime("%Y-%m-%d") + ".csv"
    if os.path.isfile(path) and (not refresh):
        return pd.read_csv(path)

    universe = investment_universe.get_SPX(rebal_date)
    fundamentals = sharadar_fundamentals.get_fundamentals(universe['ticker'].to_list(), rebal_date)
    p_fundamentals = sharadar_fundamentals.get_fundamentals(universe['ticker'].to_list(), rebal_date - timedelta(weeks=52))
    prices = sharadar_prices.get_prices(universe['ticker'].to_list(), rebal_date)
    price_df = prices[["ticker", "closeadj"]]
    exit_prices = sharadar_prices.get_prices(universe['ticker'].to_list(), date_util.get_next_rebal_day(rebal_date, 3))
    exit_prices_df = exit_prices[["ticker", "closeadj"]]

    sectors = sharadar_tickers.get_tickers(universe['ticker'].to_list(), rebal_date)
    sectors = sectors[["ticker", "sector"]]
    vol_df = sharadar_prices.get_90d_vol(universe['ticker'].to_list(), rebal_date)

    previous_month = date_util.get_previous_month_end(rebal_date)
    previous_month_df = sharadar_prices.get_prices(universe['ticker'].to_list(), previous_month)
    previous_month_df = previous_month_df[["ticker", "closeadj"]]

    previous_year = date_util.get_bus_month_end(rebal_date.year - 1, rebal_date.month)
    previous_year_df = sharadar_prices.get_prices(universe['ticker'].to_list(), previous_year)
    previous_year_df = previous_year_df[["ticker", "closeadj"]]

    fundamentals = pd.merge(fundamentals, sectors, left_on="ticker", right_on="ticker", how="inner")
    fundamentals = pd.merge(fundamentals, price_df, left_on="ticker", right_on="ticker", how="inner")
    fundamentals = pd.merge(fundamentals, exit_prices_df, left_on="ticker", right_on="ticker", how="inner", suffixes=["", "_f1w"])
    fundamentals = pd.merge(fundamentals, p_fundamentals, left_on="ticker", right_on="ticker", how="inner", suffixes=["", "_1y"])
    fundamentals = pd.merge(fundamentals, previous_month_df, left_on="ticker", right_on="ticker", how="inner", suffixes=["", "_1m"])
    fundamentals = pd.merge(fundamentals, previous_year_df, left_on="ticker", right_on="ticker", how="inner", suffixes=["", "_1y"])
    fundamentals = pd.merge(fundamentals, vol_df, left_on="ticker", right_index=True, how="inner")
    fundamentals["forward_return"] = fundamentals["closeadj_f1w"] / fundamentals["closeadj"] - 1

    fundamentals = fundamentals[["ticker", "sector", "closeadj", "closeadj_1m", "closeadj_1y", "forward_return", "Vol_90D",
                                 "assets", "cashneq", "debt","equity", "ev", "fcf", "intangibles", "liabilities", "liabilitiesc", "ncf", "revenue", "tangibles",
                                 "assets_1y", "cashneq_1y",  "debt_1y", "fcf_1y", "intangibles_1y", "liabilities_1y", "liabilitiesc_1y"]]

    fundamentals.to_csv(path)
    return fundamentals


def print_performance(pnl, dates):
    pnl = np.array(pnl)
    pnl[np.isnan(pnl)] = 0

    pnl_df = pd.DataFrame({"date": dates, "return": pnl})
    pnl_df["date"] = pd.to_datetime(pnl_df["date"])
    pnl_df.set_index("date", inplace=True)

    file.write("Full Sample:\n")
    file.write("Annual Ret: {:.2%}\n".format(np.mean(pnl) * 52))
    file.write("Annual Vol: {:.2%}\n".format(np.std(pnl) * np.sqrt(52)))
    file.write("Sharpe Ratio: {:.2f}\n".format(np.mean(pnl) / np.std(pnl) * np.sqrt(52)))
    file.write("t-Statistic: {:.2f}\n".format(stats.ttest_1samp(pnl, popmean=0).statistic))

    cum_returns = np.cumprod(pnl + 1) - 1
    high_watermark = np.maximum.accumulate(cum_returns)
    drawdown = (high_watermark - cum_returns) / (1 + high_watermark)
    file.write("Worst Drawdown: {:.2%}\n".format(np.max(drawdown)))
    
    file.write("Percent Weeks Up: {:.2%}\n".format(len(pnl[pnl >= 0]) / len(pnl)))
    file.write("Average Weekly Gain: {:.2%}\n".format(np.mean(pnl[pnl >= 0])))
    file.write("Average Weekly Loss: {:.2%}\n".format(np.mean(pnl[pnl < 0])))
    file.write("Best Week: {:.2%}\n".format(np.max(pnl)))
    file.write("Worst Week: {:.2%}\n".format(np.min(pnl)))

    file.write("2000 - 2009 Annual Ret: {:.2%}\n".format(np.mean(pnl_df.loc["2000":"2009", "return"]) * 52))
    file.write("2000 - 2009 Annual Vol: {:.2%}\n".format(np.std(pnl_df.loc["2000":"2009", "return"]) * np.sqrt(52)))
    file.write("2000 - 2009 Sharpe Ratio: {:.2f}\n".format(np.mean(pnl_df.loc["2000":"2009", "return"]) / np.std(pnl_df.loc["2000":"2009", "return"]) * np.sqrt(52)))

    file.write("2010 - 2019 Annual Ret: {:.2%}\n".format(np.mean(pnl_df.loc["2010":"2019", "return"]) * 52))
    file.write("2010 - 2019 Annual Vol: {:.2%}\n".format(np.std(pnl_df.loc["2010":"2019", "return"]) * np.sqrt(52)))
    file.write("2010 - 2019 Sharpe Ratio: {:.2f}\n".format(np.mean(pnl_df.loc["2010":"2019", "return"]) / np.std(pnl_df.loc["2010":"2019", "return"]) * np.sqrt(52)))

    file.write("2020 - 2021 Annual Ret: {:.2%}\n".format(np.mean(pnl_df.loc["2020":"2021", "return"]) * 52))
    file.write("2020 - 2021 Annual Vol: {:.2%}\n".format(np.std(pnl_df.loc["2020":"2021", "return"]) * np.sqrt(52)))
    file.write("2020 - 2021 Sharpe Ratio: {:.2f}\n".format(np.mean(pnl_df.loc["2020":"2021", "return"]) / np.std(pnl_df.loc["2020":"2021", "return"]) * np.sqrt(52)))

    file.write(pnl_df.groupby(pnl_df.index.year).sum().to_string())

    plt.plot(dates, np.cumprod(pnl + 1) - 1)
    plt.savefig(home_path + '/documents/' + model_name + '_{}.png'.format(date.today().strftime("%Y-%m-%d")))

    pnl_df.to_csv(home_path + '/documents/' + model_name + '_{}.csv'.format(date.today().strftime("%Y-%m-%d")), index=False)

    file.write("\nRun end time: {:%d/%m/%y %H:%M:%S}\n".format(datetime.now()))
    file.close()
    

if __name__ == "__main__":
    dates = []
    pnl = []
    rebal_date = date(2000, 1, 1)
    while rebal_date <= date(2021, 12, 31):
        rebal_date = date_util.get_next_rebal_day(rebal_date, 3)
        signals = get_data(rebal_date)

        if signals.empty:
            continue
        dates.append(rebal_date)

        signals.loc[signals["sector"] == "Real Estate", "sector"] = "Financial Services"

        for factor in ["tangible_asset_to_price", "ncf_to_ev", "sales_to_price", "accruals", "fcf_to_ic_growth", "momentum"]:
            func = getattr(fundamental_signal, factor)
            signals = func(signals)
            signals = math_util.normalize(signals, factor)

        signals["composite"] = (signals["tangible_asset_to_price_z"] + signals["ncf_to_ev_z"] + signals["sales_to_price_z"] + signals["accruals_z"] + signals["fcf_to_ic_growth_z"] + signals["momentum_z"]) / 6

        signals = signals.sort_values("composite", ascending=False)
        signals = signals[~signals["composite"].isna()]
        pnl.append(signals[signals["composite"] >= signals.groupby("sector")["composite"].transform("quantile", 0.75)]["forward_return"].mean() - 
                    signals[signals["composite"] <= signals.groupby("sector")["composite"].transform("quantile", 0.25)]["forward_return"].mean())

    print_performance(pnl, dates)
