from GUi import Gui
from Scraper import Scraper
from rtrigger import RScriptTrigger
import datetime as dt


def main():
    path = "project.r"
    start = dt.datetime(2021, 1, 1)
    end = dt.datetime.now()
    scraper = Scraper(start, end)
    r_trigger = RScriptTrigger(path)

    gui = Gui(title="Portfolio Optimization", scraper_obj=scraper, rtrigger_obj=r_trigger)
    gui.run()


if __name__ == "__main__":
    main()
