from abc import ABC, abstractmethod
from datetime import date
from typing import Dict, Sequence

from alpha_vantage_api import AlphaVantageAPI
from stock_api import StockAPI, StockData


class DataFetcher:
    def __init__(self, stock_api: StockAPI) -> None:
        self.stock_api = stock_api
        self.stock_data: Dict[str, StockData] = {}

    def populate_stock_data(self, symbols: Sequence[str], date: date) -> None:
        for symbol in symbols:
            print("Finding data for symbol: {}".format(symbol))
            try:
                self.stock_data[symbol] = self.stock_api.get_stock_data_for_symbol(
                    symbol, date
                )
            except Exception as e:
                print("Error fetching data for symbol: {}".format(symbol))
                print(e)
                continue


DATE = date(2015, 12, 31)
SYMBOLS = [
    "AAL",
    "AAPL",
    "ABBV",
    "ABC",
    "ABT",
    "ACN",
    "ADBE",
    "ADI",
    "ADM",
    "ADP",
    # "ADS",
    "ADSK",
    "AEE",
    "AEP",
    "AES",
    "AET",
    "AFL",
    "AGN",
    "AIG",
    "AIV",
    "AIZ",
    "AJG",
    "AKAM",
    "ALB",
    "ALGN",
    "ALK",
    "ALL",
    "ALLE",
    "ALXN",
    "AMAT",
    "AMD",
    "AME",
    "AMG",
    "AMGN",
    "AMP",
    "AMT",
    "AMZN",
    "AN",
    "ANTM",
    "AON",
    "APA",
    "APC",
    "APD",
    "APH",
    "ARG",
    "ATVI",
    "AVB",
    "AVGO",
]

data_fetcher = DataFetcher(AlphaVantageAPI())
data_fetcher.populate_stock_data(SYMBOLS, DATE)
