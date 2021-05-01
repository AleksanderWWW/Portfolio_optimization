from GUi import Gui
from Scraper import Scraper
from rtrigger import RScriptTrigger


def main():
    path = "project.r"
    scraper = Scraper()
    r_trigger = RScriptTrigger(path)

    gui = Gui(title="Portfolio Optimization", scraper_obj=scraper, rtrigger_obj= r_trigger)
    gui.run()


if __name__ == "__main__":
    main()
