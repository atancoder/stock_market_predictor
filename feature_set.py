from typing import List, NamedTuple, Tuple

from stock_api import StockData


class Feature:
    """
    Pretty simple feature set that incorportates the following:
    - PE Ratio
    - Market Cap
    - Percentage change from last year
    """

    def __init__(
        self,
        pe_ratio: float,
        market_cap: float,
        current_price: float,
        last_year_price: float,
    ) -> None:
        self.pe_ratio = pe_ratio
        self.market_cap = market_cap
        self.past_pct_change = (current_price - last_year_price) / last_year_price

    def get_vector(self) -> List[float]:
        return [self.pe_ratio, self.market_cap, self.past_pct_change]


class LabeledData(NamedTuple):
    feature: Feature
    label: float


def convert_stock_data_to_labeled_data(
    curr_stock_data: StockData, future_stock_data: StockData
) -> LabeledData:
    feature = Feature(
        pe_ratio=curr_stock_data.pe_ratio,
        market_cap=curr_stock_data.market_cap,
        current_price=curr_stock_data.price,
        last_year_price=curr_stock_data.last_year_price,
    )
    label = (future_stock_data.price - curr_stock_data.price) / curr_stock_data.price
    return LabeledData(feature=feature, label=label)
