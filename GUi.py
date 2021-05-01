import PySimpleGUI as sg
import json


class Gui:
    def __init__(self, title, scraper_obj=None, rtrigger_obj=None):
        self.title = title
        self.layout = [
            [sg.Text('Simulated Annealing')],
            [sg.Text('alpha'), sg.InputText(key="sa_alpha")],
            [sg.Text('temperature'), sg.InputText(key="sa_temperature")],
            [sg.Text('max_iter'), sg.InputText(key="sa_max_iter")],
            [sg.Button('Optimize'), sg.Button('Cancel')]
                     ]
        self.values = {}
        self.out_file = "config.json"
        self.scraper = scraper_obj
        self.r_obj = rtrigger_obj

    def create_window(self):
        window = sg.Window(self.title, self.layout)
        return window

    def create_dict(self):
        val_dict = {
            "Simulated_annealing": {key: self.values[key] for key in list(self.values.keys()) if key[:2] == "sa"}}
        return val_dict

    def save_values(self, value_dict: dict):
        with open(self.out_file, 'w+') as f:
            json.dump(value_dict, f)

    def run(self):
        window = self.create_window()
        while True:
            event, values = window.read()
            if event is None or event == 'Cancel':  # if user closes window or clicks cancel
                break
            self.values = values
            val_dict = self.create_dict()
            self.save_values(val_dict)
            # result_df = self.scraper.scrape()
            # self.r_obj.add_df(result_df)
            # self.r_obj.optimize()
        window.close()


if __name__ == "__main__":
    gui = Gui("Portfolio optimizer")
    gui.run()

