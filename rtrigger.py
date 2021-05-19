import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


class RScriptTrigger:
    """Class to store R-based functions to be triggered from external R script"""
    def __init__(self, script_path):
        self.script_path = script_path
        self.r = ro.r
        self.r_cov_df = None
        self.r_ind_er = None
        self.param_dict = None

    def source_r_script(self):
        self.r['source'](self.script_path)

    def add_py_objects(self, cov_matrix, ind_er_vector):
        self.r_cov_df = self.df_to_r_object(cov_matrix)
        self.r_ind_er = self.df_to_r_object(ind_er_vector)

    def add_result_dict(self, p_dict: dict):
        self.param_dict = p_dict

    @staticmethod
    def df_to_r_object(df):
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_from_pd_df = ro.conversion.py2rpy(df)
        return r_from_pd_df

    def simulated_annealing(self):
        params = self.param_dict["Simulated_annealing"]
        sim_ann = ro.globalenv["simulated_annealing"]

    def particle_swarm(self):
        params = self.param_dict["Particle_swarm"]
        pass

    def optimize(self):
        pass
