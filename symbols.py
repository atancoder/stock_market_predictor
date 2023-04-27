from typing import List

import pandas as pd


def get_sp500_stocks() -> List[str]:
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    table = pd.read_html(url, header=0)[0]
    symbols: List[str] = table["Symbol"].tolist()
    return symbols


SYMBOLS = get_sp500_stocks()
