import numpy as np
import pandas as pd


def factor_quantile_table(data):
    negative_opermargin = data[data <= 0]
    twenty_five_percentile = np.nanpercentile(negative_opermargin, 50)
    first_quantile = negative_opermargin[negative_opermargin <= twenty_five_percentile]
    second_quantile = negative_opermargin[negative_opermargin > twenty_five_percentile]

    positive_opermargin = data[data > 0]
    seventy_five_percentile = np.nanpercentile(positive_opermargin, 50)
    third_quantile = positive_opermargin[positive_opermargin <= seventy_five_percentile]
    forth_quantile = positive_opermargin[positive_opermargin > seventy_five_percentile]

    days_count = 1
    total_count = len(data)
    factor_quantile = {"Factor Quantile": ["1 (most negative)", "2", "3", "4 (most negative)"],
    "min": [min(first_quantile), min(second_quantile), min(third_quantile), min(forth_quantile)],
    "max": [max(first_quantile), max(second_quantile), max(third_quantile), max(forth_quantile)],
    "mean": [np.mean(first_quantile), np.mean(second_quantile), np.mean(third_quantile), np.mean(forth_quantile)],
    "std": [np.std(first_quantile), np.std(second_quantile), np.std(third_quantile), np.std(forth_quantile)],
    "count": [len(first_quantile), len(second_quantile), len(third_quantile), len(forth_quantile)],
    "avg daily count": [len(first_quantile) / days_count, len(second_quantile) / days_count, len(third_quantile) / days_count, len(forth_quantile) / days_count],
    "count %": [len(first_quantile) / total_count, len(second_quantile) / total_count, len(third_quantile) / total_count, len(forth_quantile) / total_count]}

    factor_quantile_df = pd.DataFrame(factor_quantile)
    factor_quantile_df.set_index("Factor Quantile", inplace=True)
    return factor_quantile_df


def factor_quantile_return(data, field):
    negative_opermargin = data[data[field] <= 0][field]
    twenty_five_percentile = np.nanpercentile(negative_opermargin, 50)

    positive_opermargin = data[data[field] > 0][field]
    seventy_five_percentile = np.nanpercentile(positive_opermargin, 50)
    
    firstq_returns = data[data[field] <= twenty_five_percentile][["OneDRet", "FiveDRet", "TwentyOneDRet"]].median()
    secondq_returns = data[(data[field] > twenty_five_percentile) & (data[field] <= 0) ][["OneDRet", "FiveDRet", "TwentyOneDRet"]].median()
    thirdq_returns = data[(data[field] > 0) & (data[field] <= seventy_five_percentile) ][["OneDRet", "FiveDRet", "TwentyOneDRet"]].median()
    forthq_returns = data[(data[field] > seventy_five_percentile) ][["OneDRet", "FiveDRet", "TwentyOneDRet"]].median()

    one_day_returns = [firstq_returns[0], secondq_returns[0], thirdq_returns[0], forthq_returns[0]]
    five_day_returns = [firstq_returns[1], secondq_returns[1], thirdq_returns[1], forthq_returns[1]]
    twentyone_day_returns = [firstq_returns[2], secondq_returns[2], thirdq_returns[2], forthq_returns[2]]

    return one_day_returns, five_day_returns, twentyone_day_returns
