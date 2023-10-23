def gross_margin(data):
    """
    Return an gross margin factor
    """
    data["gross_margin"] = (data.revenue - data.cor) / data.assets
    return data


def return_on_equity(data):
    """
    Return an return on equity factor
    """
    data["return_on_equity"] = data.eps / data.bvps
    return data


def operating_leverage(data):
    """
    Return an opearating leverage factor
    """
    data["operating_leverage"] = (data.assets - data.equity - data.debt) / (data.equity + data.debt - data.cashneq)
    return data