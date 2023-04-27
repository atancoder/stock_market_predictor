import random
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import date
from typing import Dict, List, Sequence, Tuple

from alpha_vantage_api import AlphaVantageAPI
from feature_set import LabeledData, convert_stock_data_to_labeled_data
from stock_api import StockAPI, StockData
from symbols import INVALID_SYMBOLS, SYMBOLS, save_as_txt


class DataFetcher:
    def __init__(
        self, stock_api: StockAPI, curr_date: date, predictor_date: date
    ) -> None:
        self.stock_api = stock_api
        self.stock_data: Dict[str, Dict[date, StockData]] = defaultdict(dict)
        self.curr_date = curr_date
        self.predictor_date = predictor_date

    def populate_stock_data(self, symbols: Sequence[str]) -> None:
        invalid_symbols = INVALID_SYMBOLS
        for symbol in symbols:
            if symbol in invalid_symbols:
                continue
            try:
                self.stock_data[symbol][
                    self.curr_date
                ] = self.stock_api.get_stock_data_for_symbol(symbol, self.curr_date)
                self.stock_data[symbol][
                    self.predictor_date
                ] = self.stock_api.get_stock_data_for_symbol(
                    symbol, self.predictor_date
                )
            except Exception as e:
                print("Error fetching data for symbol: {}".format(symbol))
                print(e)
                invalid_symbols.append(symbol)
                continue
        save_as_txt(invalid_symbols, "invalid_symbols.txt")

    def get_labeled_data(self) -> List[LabeledData]:
        labeled_data: List[LabeledData] = []
        for symbol, data in self.stock_data.items():
            if self.curr_date in data and self.predictor_date in data:
                labeled_data.append(
                    convert_stock_data_to_labeled_data(
                        data[self.curr_date], data[self.predictor_date]
                    )
                )
        return labeled_data


def split_data(
    labeled_data: List[LabeledData],
    training_set_pct: int = 70,
    test_set_pct: int = 20,
    validation_set_pct: int = 10,
) -> Tuple[List[LabeledData], List[LabeledData], List[LabeledData]]:
    if training_set_pct + test_set_pct + validation_set_pct != 100:
        raise ValueError("Percentages must add up to 1")
    training_set_size = int(len(labeled_data) * training_set_pct / 100)
    test_set_size = int(len(labeled_data) * test_set_pct / 100)
    validation_set_size = int(len(labeled_data) * validation_set_pct / 100)
    random.shuffle(labeled_data)

    training_set = labeled_data[:training_set_size]
    test_set = labeled_data[training_set_size : training_set_size + test_set_size]
    validation_set = labeled_data[-validation_set_size:]
    return training_set, test_set, validation_set
