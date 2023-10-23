# Quality
def gross_margin(data):
    data["gross_margin"] = (data.revenue - data.cor) / data.assets
    return data


def operating_leverage(data):
    data["operating_leverage"] = (data.assets - data.equity - data.debt) / (data.equity + data.debt - data.cashneq)
    return data


def return_on_equity(data):
    data["return_on_equity"] = data.eps / data.bvps
    return data


# Value
def dividend_yield(data):
    data["dividend_yield"] = data["divyield"]
    return data


def earnings_to_price(data):
    data["earnings_to_price"] = data["eps"] / data["price"]
    return data


def ofcf_to_ev(data):
    data["ofcf_to_ev"] = data["ncfo"] / data["ev"]
    return data


def tangible_book_to_price(data):
    data["tangible_book_to_price"] = data["tangibles"] / data["marketcap"]
    return data