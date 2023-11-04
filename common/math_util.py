import numpy as np
from scipy import stats


def normalize(df, factor):
    df[factor + "_z"] = df.groupby("sector", group_keys=False)[factor].apply(lambda x: (x - np.mean(x)) / np.std(x)).clip(-3, 3)
    for i in range(5):
        if stats.normaltest(df[factor + "_z"]).pvalue > 0.05:
            break
        df[factor + "_z"] = df.groupby("sector", group_keys=False)[factor + "_z"].apply(lambda x: (x - np.mean(x)) / np.std(x)).clip(-3, 3)
    return df