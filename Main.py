from GUi import Gui
from Scraper import Scraper
from simulated_annealing import *
import datetime as dt


def main():
    end = dt.datetime.now()
    start = end - dt.timedelta(days=365*2)
    scraper = Scraper(start, end)
    gui = Gui(title="Portfolio Optimization", scraper_obj=scraper, annealer_obj=AnnealingEngine, obj_func=obj_func)
    gui.run()


if __name__ == "__main__":
    main()
