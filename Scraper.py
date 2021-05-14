import requests
from bs4 import BeautifulSoup
from math import ceil
import pandas as pd
import datetime as dt
import pandas_datareader as pdr
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor as Executor


class Scraper:
    base_url = "https://stooq.pl/t/?i=513"

    def __init__(self, start_date, end_date):
        self.start = start_date
        self.end = end_date
        self.all_dfs = []
        self.data = pd.DataFrame()
        self.tickers = []

    def get_tickers(self):
        html = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = BeautifulSoup(html.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            ticker = ticker[:-1]
            self.tickers.append(ticker)

    def get_time_series(self, ticker):
        df = pdr.DataReader(ticker.replace('.', '-'), 'yahoo', self.start, self.end)
        df = df["Adj Close"]
        df = df.rename(ticker)
        self.all_dfs.append(df)

    def scrape_data(self):
        self.get_tickers()
        with Executor(max_workers=40) as executor:
            executor.map(self.get_time_series, self.tickers)
        self.data = self.merge_data_frames(self.all_dfs)
        #pool = mp.Pool(mp.cpu_count())
        #[pool.apply(self.get_time_series, args=(ticker,)) for ticker in self.tickers]
        #pool.close()
        #for ticker in self.tickers[:5]:
            #self.get_time_series(ticker=ticker)

    @staticmethod
    def calculate_pagination(number_records):
        """This function will calculate how many pages need to be scraped, based on the total number of records,
        since we know that there are max 100 records per page"""
        n = ceil(number_records/100)
        return n

    def create_soup(self, page_num):
        r = requests.get(self.base_url+"&v=0&l="+str(page_num))
        soup = BeautifulSoup(r.text, 'lxml')
        return soup

    def get_num_records(self):
        r = requests.get(self.base_url)
        soup = BeautifulSoup(r.text, 'lxml')
        text = soup.find("td", {"id": "f13"}).text
        record_num = text.split("|")[0].split(" ")[-2]
        return soup, int(record_num)

    @staticmethod
    def extract_table(page_soup):
        data = []
        table = page_soup.find("table", {"id": "fth1"})
        header = ["Symbol",	"Nazwa", "Kurs", "Zmiana1", "Zmiana2", "Wolumen"]
        table = table.find("tbody")
        for row in table.find_all("tr"):
            cell_list = [cell.text for cell in row.find_all('td')][:-2]
            data.append(cell_list)
        df = pd.DataFrame(data, columns=header)
        return df

    @staticmethod
    def merge_data_frames(dfs):
        df = pd.concat(dfs, axis=1)
        return df

    def scrape(self):
        soup, num = self.get_num_records()
        num_of_pages = self.calculate_pagination(num)
        df1 = self.extract_table(soup)
        self.all_dfs.append(df1)
        for i in range(2, num_of_pages+1):
            page_soup = self.create_soup(i)
            df = self.extract_table(page_soup)
            self.all_dfs.append(df)
        result = self.merge_data_frames(self.all_dfs)
        return result


if __name__ == "__main__":
    start = dt.datetime(2021, 1, 1)
    end = dt.datetime.now()
    scraper = Scraper(start, end)
    scraper.scrape_data()
    print(scraper.data)
