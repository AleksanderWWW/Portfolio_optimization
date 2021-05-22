import PySimpleGUI as sg
from preprocessing import *
import pandas as pd


class Gui:
    def __init__(self, title, scraper_obj=None, annealer_obj=None, obj_func=None):
        self.title = title
        self.layout = [
            [sg.Text('Simulated Annealing')],
            [sg.Text('alpha          '), sg.InputText(key="sa_alpha")],
            [sg.Text('temperature'), sg.InputText(key="sa_temperature")],
            [sg.Text('neighbourhood distance'), sg.InputText(key="sa_dist")],
            [sg.Text('max_iter     '), sg.InputText(key="sa_max_iter")],
            [sg.Button('Optimize'), sg.Button('Cancel')],
            [sg.Output(size=(100, 350))]
                     ]
        self.values = {}
        self.out_file = "config.json"
        self.scraper = scraper_obj
        self.annealer = annealer_obj
        self.window = self.create_window()
        self.obj_func = obj_func
        self.df = None

    def create_window(self):
        window = sg.Window(self.title, self.layout, size=(690, 450))
        return window

    def initialize_annealer(self, val_dict):
        cov_matrix = get_cov_matrix(self.df)
        ind_er = get_ind_er(self.df)
        try:
            annealer = self.annealer(self.obj_func, cov_matrix, ind_er, len(self.df.columns),
                                     float(val_dict["sa_temperature"]),
                                     float(val_dict["sa_dist"]),
                                     float(val_dict["sa_alpha"]),
                                     float(val_dict["sa_max_iter"]))
        except ValueError:
            # if input is incorrect the program will launch optimization with default parameters
            self.display_output("Incorrect input. The program will launch optimization with default parameters.")
            annealer = self.annealer(self.obj_func, cov_matrix, ind_er, len(self.df.columns))

        return annealer

    def display_output(self, msg):
        print(msg)
        self.window.refresh()

    def run(self):
        while True:
            event, values = self.window.read()
            if event is None or event == 'Cancel':  # if user closes window or clicks cancel
                break
            self.values = values
            self.display_output("Scraping stock values...")
            #self.scraper.scrape_data()
            #self.df = self.scraper.data
            self.df = pd.read_excel("temp.xlsx")
            self.df = self.df.set_index("Date")
            self.display_output("Scraping complete")
            self.display_output("Performing optimization...")
            annealer = self.initialize_annealer(values)
            annealer.optimize()
            result = annealer.get_result
            try:
                weights, sharpe = result
                self.display_output("Optimization successful")
                self.display_output(f"Portfolio weights: {weights}")
                self.display_output(f"Sharpe ratio: {sharpe}")
            except Exception as e:
                self.display_output(f"Optimization unsuccessful: {e}")

        self.window.close()


if __name__ == "__main__":
    gui = Gui("Portfolio optimizer")
    gui.run()

