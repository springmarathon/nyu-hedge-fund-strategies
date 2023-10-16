"""https://data.nasdaq.com/databases/SEP/documentation"""
import datetime
import nasdaqdatalink as quandl
import pandas as pd


def get_price_daterange(ticker, as_of_date):
    """ To retrieve data for a specified data range """
    gte = as_of_date.strftime("%Y-%m-%d")
    lte = (as_of_date + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    return quandl.get_table('SHARADAR/SEP', date={'gte': gte, 'lte': lte}, ticker=ticker)



if __name__ == "__main__":
    quandl.ApiConfig.api_key = 'NRvcyMwNMXZ2ooDSM3nw'
    df = get_price_daterange('ZTS', pd.Timestamp('2023-08-08 00:00:00'))
    print(df)
