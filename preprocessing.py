import pandas as pd


def add_stats(df: pd.DataFrame):
    ret_list = []
    var_list = []
    for col in df.columns:
        ret = (df[col][-1] - df[col][0])/df[col][0]
        ret_list.append(ret)
        var = df[col].var()
        var_list.append(var)
    df.loc["Variance"] = var_list
    df.loc["ROR"] = ret_list
    return df


data = pd.read_excel("temp.xlsx")
data = data.set_index("Date")
df = add_stats(data)
breakpoint()
