import numpy as np
import numpy_financial as npf


# Quality
def cfroi(data):
    data["non_depre_assets"] = np.nansum([data["investments"], data["ppnenet"]], axis=0) / data["shareswa"]
    data["cfroi"] = 0
    for i in range(data.shape[0]):
        if (~np.isnan(data.loc[i, "price"])) and (~np.isnan(data.loc[i, "non_depre_assets"])):
            cf = np.nansum([data.loc[i, "eps"], data.loc[i, "dps"]]) / 2.0 if np.isnan(data.loc[i, "fcfps"]) else data.loc[i, "fcfps"]
            data.loc[i, "cfroi"] = npf.irr(np.append(np.append(-1 * data.loc[i, "price"], 1.03 ** np.arange(0, 19) * cf), 1.03 ** 20 * cf + data.loc[i, "non_depre_assets"]))
    return data


def debt_to_equity(data):
    data["debt_to_equity"] = data["debt"] / data["equity"]
    return data


def gross_margin(data):
    data["gross_margin"] = (data.revenue - data.cor) / data.assets
    return data


def margin(data):
    data["margin"] = (data.revenue - data.cor - data.sgna - data["intexp"]) / data["assets"]
    return data


def operating_leverage(data):
    data["operating_leverage"] = (data.assets - data.equity - data.debt) / (data.equity + data.debt - data.cashneq)
    return data


def operating_margin(data):
    data["operating_margin"] = data["opinc"] / data["revenue"]
    return data


def return_on_equity(data):
    data["return_on_equity"] = data["netinc"] / data["equity"]
    return data


def return_on_invcap(data):
    data["return_on_invcap"] = data["netinc"] / data["invcap"]
    return data


# Value
def book_to_price(data):
    data["book_to_price"] = data["equity"] / data["marketcap"]
    return data


def dividend_yield(data):
    data["dividend_yield"] = data["divyield"]
    return data


def earnings_to_price(data):
    data["earnings_to_price"] = data["eps"] / data["price"]
    return data


def fcf_to_ev(data):
    data["fcf_to_ev"] = data["fcf"] / data["ev"]
    return data


def fcf_to_price(data):
    data["fcf_to_price"] = data["fcfps"] / data["price"]
    return data


def ncfo_to_ev(data):
    data["ncfo_to_ev"] = data["ncfo"] / data["ev"]
    return data


def ncf_to_mc(data):
    data["ncf_to_mc"] = data["ncf"] / data["marketcap"]
    return data


def sales_to_price(data):
    data["sales_to_price"] = data["revenue"] / data["marketcap"]
    return data


def tangible_book_to_price(data):
    data["tangible_book_to_price"] = data["tangibles"] / data["marketcap"]
    return data