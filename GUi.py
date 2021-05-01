import PySimpleGUI as sg
import json


class Gui:
    def __init__(self, title, scraper_obj=None, rtrigger_obj=None):
        self.title = title
        self.layout = [
            [sg.Text('Simulated Annealing')],
            [sg.Text('alpha          '), sg.InputText(key="sa_alpha")],
            [sg.Text('temperature'), sg.InputText(key="sa_temperature")],
            [sg.Text('max_iter     '), sg.InputText(key="sa_max_iter")],
            [sg.Button('Optimize'), sg.Button('Cancel')],
            [sg.Output(size=(100, 350))]
                     ]
        self.values = {}
        self.out_file = "config.json"
        self.scraper = scraper_obj
        self.r_obj = rtrigger_obj
        self.window = self.create_window()

    def create_window(self):
        window = sg.Window(self.title, self.layout, size=(690, 350))
        return window

    def create_dict(self):
        val_dict = {
            "Simulated_annealing": {key: self.values[key] for key in list(self.values.keys()) if key[:2] == "sa"}}
        return val_dict

    def save_values(self, value_dict: dict):
        with open(self.out_file, 'w+') as f:
            json.dump(value_dict, f)

    def display_output(self, msg):
        print(msg)
        self.window.refresh()

    def run(self):
        while True:
            event, values = self.window.read()
            if event is None or event == 'Cancel':  # if user closes window or clicks cancel
                break
            self.values = values
            val_dict = self.create_dict()
            # self.save_values(val_dict)
            # self.r_obj.add_result_dict(val_dict)
            self.display_output("Scraping stock values...")
            result_df = self.scraper.scrape()
            self.display_output("Scraping complete")
            self.display_output("Feeding to the optimization script...")
            # self.r_obj.add_df(result_df)
            self.display_output("Optimizing...")
            # self.r_obj.optimize()
            self.display_output("Optimization successful")
            self.display_output("View your results in results.xlsx")
        self.window.close()


if __name__ == "__main__":
    gui = Gui("Portfolio optimizer")
    gui.run()

