from preprocessing import *
import pandas as pd
from simulated_annealing import *

"""This script performs a simulation of 100 optimization processes with various combinations of the maximal iteration
number and alpha parameter."""


df = pd.read_excel("temp.xlsx")
df = df.set_index("Date")
cov_matrix = get_cov_matrix(df)
ind_er = get_ind_er(df)
all_data = []
iters = np.linspace(100, 1000, 10)
alphas = np.linspace(0.970, 0.990, 10)
# Simulate optimizations for different combinations of alpha and max_iter
for max_iter in iters:
    for alpha in alphas:
        annealer = AnnealingEngine(obj_func, cov_matrix, ind_er, len(df.columns), 100, alpha, max_iter)
        annealer.optimize()
        weights, sharpe = annealer.get_result
        data_row = [max_iter, alpha, sharpe] + list(weights)
        all_data.append(data_row)
columns = ["Max iters", "Alpha", "Sharpe ratio"] + [f"{ticker} weight" for ticker in df.columns]
result_df = pd.DataFrame(all_data, columns=columns)
result_df.to_excel("Simulation_results.xlsx", index=False)
