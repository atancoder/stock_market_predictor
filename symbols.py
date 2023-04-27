from typing import List

import pandas as pd


def save_as_txt(symbols: List[str], filename: str) -> None:
    with open(filename, "w") as f:
        for symbol in symbols:
            f.write(symbol + "\n")


def load_symbols_from_txt(filename: str) -> List[str]:
    with open(filename, "r") as f:
        symbols = f.read().splitlines()
    return symbols


def get_sp500_stocks() -> List[str]:
    try:
        symbols = load_symbols_from_txt("symbols.txt")
    except FileNotFoundError:
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        table = pd.read_html(url, header=0)[0]
        symbols = table["Symbol"].tolist()
        save_as_txt(symbols, "symbols.txt")
    return symbols


def get_invalid_symbols() -> List[str]:
    try:
        return load_symbols_from_txt("invalid_symbols.txt")
    except FileNotFoundError:
        return []


SYMBOLS = get_sp500_stocks()
INVALID_SYMBOLS = get_invalid_symbols()
