import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import pandas_datareader as pdr
from concurrent.futures import ThreadPoolExecutor as Executor


class Scraper:

    def __init__(self, start_date, end_date):
        self.start = start_date
        self.end = end_date
        self.all_dfs = []
        self.data = pd.DataFrame()
        self.tickers = []

    def get_tickers(self):
        html = requests.get("https://stooq.pl/q/i/?s=^dji")
        soup = BeautifulSoup(html.text, 'lxml')
        table = soup.find("table", {"id": "fth1"}).find("tbody")
        for row in table.find_all("tr"):
            ticker_cell = row.find("td")
            ticker = ticker_cell.text
            self.tickers.append(ticker[:-3])

    def get_time_series(self, ticker):
        df = pdr.DataReader(ticker, 'yahoo', self.start, self.end)
        df = df["Adj Close"]
        df = df.rename(ticker)
        self.all_dfs.append(df)

    def scrape_data(self):
        self.get_tickers()
        with Executor(max_workers=30) as executor:
            executor.map(self.get_time_series, self.tickers)
        self.data = self.merge_data_frames(self.all_dfs)
        self.data = self.data.sort_index(axis=1)

    @staticmethod
    def merge_data_frames(dfs):
        df = pd.concat(dfs, axis=1)
        return df


if __name__ == "__main__":
    end = dt.datetime.now()
    start = end - dt.timedelta(days=365*2)
    scraper = Scraper(start, end)
    scraper.scrape_data()
    print(scraper.data)
    scraper.data.to_excel("temp.xlsx")
