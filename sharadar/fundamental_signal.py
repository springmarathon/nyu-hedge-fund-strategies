def operating_margin(data):
    """
    Return an operating margin factor
    """
    revenue = data.revenue
    data["operating_margin"] = data.opinc / revenue.where(revenue > 0)

    # exclude companies with negative operating expenses or negative cost of revenue
    opex = data.opex
    cor = data.cor
    data["operating_margin"] = data["operating_margin"].where((opex > 0) & (cor > 0))

    # clip range to (-1, 1) so as not to overweight outliers
    data["operating_margin"] = data["operating_margin"].clip(-1, 1)

    return data