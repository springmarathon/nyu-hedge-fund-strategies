import nasdaqdatalink as quandl
import os
import pandas as pd
from datetime import date


def get_SPX(as_of_date, refresh=False):
    path = "/Users/weizhang/Documents/_GIT/quant-strategies/data/Sharadar/sp500/sp500_" + as_of_date.strftime("%Y-%m-%d") + ".csv"
    if os.path.isfile(path) and (not refresh):
        return pd.read_csv(path)

    previous_year_end = date(as_of_date.year - 1, 12, 31)
    universe = quandl.get_table('SHARADAR/SP500', action='historical', date=previous_year_end.strftime("%Y-%m-%d"))
    changes = quandl.get_table('SHARADAR/SP500', action=['added', 'removed'], date={'gte': previous_year_end.strftime("%Y-%m-%d"), 'lte': as_of_date.strftime("%Y-%m-%d")})

    universe = pd.concat([universe, changes[changes["action"] == "added"]])
    universe = pd.merge(universe, changes[changes["action"] == "removed"], left_on="ticker", right_on="ticker", how="left", suffixes=("", "_c"))
    universe = universe.loc[universe["action_c"] != "removed"].iloc[:, :7]
    # universe = universe.drop_duplicates("name", keep="first")
    universe.to_csv(path)
    return universe


if __name__ == "__main__":
    quandl.ApiConfig.api_key = 'NRvcyMwNMXZ2ooDSM3nw'
    constituents = get_SPX(date(2004, 3, 31))