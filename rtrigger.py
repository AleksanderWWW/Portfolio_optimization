import rpy2.robjects as ro


class RScriptTrigger:
    """Class to store R-based functions to be triggered from  external R scripts"""
    def __init__(self, sa_path, ts_path, gen_path, ant_path):
        self.sa_path = sa_path
        self.ts_path = ts_path
        self.gen_path = gen_path
        self.ant_path = ant_path
        self.r = ro.r

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
