import random
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import date
from typing import Dict, List, Sequence, Tuple

from alpha_vantage_api import AlphaVantageAPI
from feature_set import LabeledData, convert_stock_data_to_labeled_data
from stock_api import StockAPI, StockData
from symbols import SYMBOLS

DATE = date(2015, 12, 31)
TWO_YEARS_LATER = date(2017, 12, 31)


class DataFetcher:
    def __init__(self, stock_api: StockAPI) -> None:
        self.stock_api = stock_api
        self.stock_data: Dict[str, Dict[date, StockData]] = defaultdict(dict)

    def populate_stock_data(self, symbols: Sequence[str], date: date) -> None:
        for symbol in symbols:
            print("Finding data for symbol: {}".format(symbol))
            try:
                self.stock_data[symbol][
                    date
                ] = self.stock_api.get_stock_data_for_symbol(symbol, date)
            except Exception as e:
                print("Error fetching data for symbol: {}".format(symbol))
                print(e)
                continue

    def get_labeled_data(self) -> List[LabeledData]:
        labeled_data: List[LabeledData] = []
        for symbol, data in self.stock_data.items():
            if DATE in data and TWO_YEARS_LATER in data:
                labeled_data.append(
                    convert_stock_data_to_labeled_data(
                        data[DATE], data[TWO_YEARS_LATER]
                    )
                )
        return labeled_data


def split_data(
    labeled_data: List[LabeledData],
    training_set_pct: float = 0.7,
    test_set_pct: float = 0.2,
    validation_set_pct: float = 0.1,
) -> Tuple[List[LabeledData], List[LabeledData], List[LabeledData]]:
    if training_set_pct + test_set_pct + validation_set_pct != 1:
        raise ValueError("Percentages must add up to 1")
    training_set_size = int(len(labeled_data) * training_set_pct)
    test_set_size = int(len(labeled_data) * test_set_pct)
    validation_set_size = int(len(labeled_data) * validation_set_pct)
    random.shuffle(labeled_data)

    training_set = labeled_data[:training_set_size]
    test_set = labeled_data[training_set_size : training_set_size + test_set_size]
    validation_set = labeled_data[-validation_set_size:]
    return training_set, test_set, validation_set


def main() -> None:
    data_fetcher = DataFetcher(AlphaVantageAPI())
    data_fetcher.populate_stock_data(SYMBOLS, DATE)
    data_fetcher.populate_stock_data(SYMBOLS, TWO_YEARS_LATER)
    labeled_data = data_fetcher.get_labeled_data()
    training_set, test_set, validation_set = split_data(labeled_data)


if __name__ == "__main__":
    main()

