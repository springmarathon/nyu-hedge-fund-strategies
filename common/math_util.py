import numpy as np


def normalize(df, factor):
    df[factor + "_z"] = df.groupby("sector", group_keys=False)[factor].apply(lambda x: (x - np.mean(x)) / np.std(x)).clip(-3, 3)
    for i in range(1):
        df[factor + "_z"] = df.groupby("sector", group_keys=False)[factor + "_z"].apply(lambda x: (x - np.mean(x)) / np.std(x)).clip(-3, 3)
    return df