import PySimpleGUI as sg
import json


class Gui:
    def __init__(self, title, layout, scraper_obj=None):
        self.title = title
        self.layout = layout
        self.values = {}
        self.out_file = "config.json"
        self.scraper = scraper_obj

    def create_window(self):
        window = sg.Window(self.title, self.layout)
        return window

    def create_dict(self):
        val_dict = {}
        val_dict["Simulated_annealing"] = {key: self.values[key] for key in list(self.values.keys()) if key[:2] == "sa"}
        return val_dict

    def save_values(self, value_dict: dict):
        with open(self.out_file, 'w+') as f:
            json.dump(value_dict, f)

    def run(self):
        window = self.create_window()
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                break
            self.values = values
            val_dict = self.create_dict()
            self.save_values(val_dict)
            # self.scraper.scrape()
        window.close()


if __name__ == "__main__":
    layout = [
            [sg.Text('Simulated Annealing')],
            [sg.Text('alpha'), sg.InputText(key="sa_alpha")],
            [sg.Text('temperature'), sg.InputText(key="sa_temperature")],
            [sg.Text('max_iter'), sg.InputText(key="sa_max_iter")],
            [sg.Button('Optimize'), sg.Button('Cancel')]
            ]
    gui = Gui("Portfolio optimizer", layout)
    gui.run()

