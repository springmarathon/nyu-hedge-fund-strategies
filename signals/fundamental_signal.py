import numpy as np
import numpy_financial as npf


# Difference between the reported (accrual) earnings and cash earnings, divided by total assets
def accruals(data):
    data["accruals"] = -1.0 * (((data["assets"] - data["cashneq"]) - (data["assets_1y"] - data["cashneq_1y"])) - ((data["liabilities"] - data["debt"]) - (data["liabilities_1y"] - data["debt_1y"]))) / (data["assets"] + data["assets_1y"]) * 2
    return data


def cfroi(data):
    data["non_depre_assets"] = np.nansum([data["workingcapital"], data["investments"], data["ppnenet"]], axis=0) / data["sharesbas"]
    data["cfroi"] = 0
    data["cf"] = data["ncf"] / data["shareswa"]
    for i in range(data.shape[0]):
        if (~np.isnan(data.loc[i, "price"])) and (~np.isnan(data.loc[i, "non_depre_assets"])):
            cf = np.nansum([data.loc[i, "eps"], data.loc[i, "dps"]]) / 2.0 if np.isnan(data.loc[i, "cf"]) else data.loc[i, "cf"]
            # fv = data.loc[i, "non_depre_assets"] if np.isnan(data.loc[i, "tbvps"]) else data.loc[i, "tbvps"]
            fv = data.loc[i, "tbvps"] if np.isnan(data.loc[i, "non_depre_assets"]) else data.loc[i, "non_depre_assets"]
            data.loc[i, "cfroi"] = npf.irr(np.append(np.append(-1 * data.loc[i, "price"], 1.03 ** np.arange(0, 19) * cf), 1.03 ** 20 * cf + fv))
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


def net_profit_margin(data):
    data["net_profit_margin"] = data["netinc"] / data["revenue"]
    return data


def operating_leverage(data):
    data["operating_leverage"] = (data["liabilities"] - data.debt) / (data.equity + data.debt - data.cashneq)
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


def book_to_price(data):
    data["book_to_price"] = data["equity"] / data["marketcap"]
    return data


def dividend_yield(data):
    data["dividend_yield"] = data["dps"] / data["price"]
    return data


def earnings_yield(data):
    data["earnings_yield"] = data["eps"] / data["price"]
    return data


def fcf_to_ev(data):
    data["fcf_to_ev"] = data["fcf"] / data["ev"]
    return data


def fcf_yield(data):
    data["fcf_yield"] = data["fcf"] / data["marketcap"]
    return data


def ncfo_to_ev(data):
    data["ncfo_to_ev"] = data["ncfo"] / data["ev"]
    return data


def ncfo_to_mc(data):
    data["ncfo_to_mc"] = data["ncfo"] / (data.equity + data.debt - data.cashneq)
    return data


def fcf_to_ic_growth(data):
    data["fcf_to_ic_growth"] = data["fcf"] / (data["debt"] + data["assets"] - data["intangibles"] - data["cashneq"] - data["liabilitiesc"]) - data["fcf_1y"] / (data["debt_1y"] + data["assets_1y"] - data["intangibles_1y"] - data["cashneq_1y"] - data["liabilitiesc_1y"]) 
    return data


#V1
def ncf_to_ev(data):
    data["ncf_to_ev"] = data["ncf"] / data["ev"]
    return data


def ncf_to_mc(data):
    data["ncf_to_mc"] = data["ncf"] / (data.equity + data.debt - data.cashneq)
    return data

#V1
def sales_to_price(data):
    data["sales_to_price"] = data["revenue"] / (data.equity + data.debt - data.cashneq)
    return data

#V1
def tangible_asset_to_price(data):
    data["tangible_asset_to_price"] = data["tangibles"] / (data.equity + data.debt - data.cashneq)
    return data