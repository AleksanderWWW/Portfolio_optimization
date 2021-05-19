import numpy as np

"""Moduł ma za zadanie dostarczyć do skryptu R przeprocesowane dane, uzyskane na bazie tabeli z 
    notowaniami giełdowymi"""


def get_cov_matrix(df):
    """Zwraca macierz kowariancji, na podstawie której wyliczone zostanie volatility"""
    new_df = df.copy()
    new_df = new_df.pct_change().apply(lambda x: np.log(1 + x))
    return new_df.cov()


def get_ind_er(df):
    """Zwraca wektor, który po wymnożeniu przez wektor wag da zwrot z portfela"""
    ind_er = df.resample('Y').last().pct_change().mean()
    return ind_er


