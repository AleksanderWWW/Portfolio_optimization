import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


class RScriptTrigger:
    """Class to store R-based functions to be triggered from external R script"""
    def __init__(self, script_path):
        self.script_path = script_path
        self.r = ro.r
        self.r_df = None

    def source_r_script(self):
        self.r['source'](self.script_path)

    def add_df(self, df):
        self.r_df = self.df_to_r_object(df)

    @staticmethod
    def df_to_r_object(df):
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_from_pd_df = ro.conversion.py2rpy(df)
        return r_from_pd_df

    def simAnnealing(self):
        pass

    def tabuSearch(self):
        pass

    def genAlgorithm(self):
        pass

    def antColony(self):
        pass

    def optimize(self):
        pass
