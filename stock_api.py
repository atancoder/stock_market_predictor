from abc import ABC, abstractmethod
from datetime import date


class StockData:
    def __init__(
        self,
        symbol: str,
        date: date,
        price: float,
        PE_ratio: float,
        industry: str,
        sector: str,
        market_cap: float,
        dividend_yield: float,
        last_year_price: float,
    ) -> None:
        self.symbol = symbol
        self.date = date

        self.price = price
        self.PE_ratio = PE_ratio
        self.industry = industry
        self.sector = sector
        self.market_cap = market_cap
        self.last_year_price = last_year_price


class StockAPI(ABC):
    @abstractmethod
    def get_stock_data_for_symbol(self, symbol: str, date: date) -> StockData:
        pass
