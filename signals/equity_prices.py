"""https://data.nasdaq.com/databases/SEP/documentation"""
import datetime
import nasdaqdatalink as quandl
import pandas as pd


def get_price_daterange(tickers, start_date, end_date=None):
    """ To retrieve data for a specified data range """
    gte = start_date.strftime("%Y-%m-%d")
    if end_date is None:
        lte = (start_date + datetime.timedelta(days=40)).strftime("%Y-%m-%d")
    else:
        lte = end_date.strftime("%Y-%m-%d")
    return quandl.get_table('SHARADAR/SEP', date={'gte': gte, 'lte': lte}, ticker=tickers)



if __name__ == "__main__":
    quandl.ApiConfig.api_key = 'NRvcyMwNMXZ2ooDSM3nw'
    df = get_price_daterange(['VLTO'], pd.Timestamp('2023-08-31 00:00:00'))
    print(df)
