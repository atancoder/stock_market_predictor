import math
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


class Standardizer:
    def __init__(self, features: List[Feature]) -> None:
        self.initial_features = features
        self.means: List[float] = []
        self.stds: List[float] = []
        self.compute_means_and_stds()

    def compute_means_and_stds(self) -> None:
        num_features = len(self.initial_features[0].get_vector())
        self.means = [0] * num_features
        self.stds = [0] * num_features
        for feature in self.initial_features:
            for i, feature_component in enumerate(feature.get_vector()):
                self.means[i] += feature_component
        for i in range(num_features):
            self.means[i] /= len(self.initial_features)
        for feature in self.initial_features:
            for i, feature_component in enumerate(feature.get_vector()):
                self.stds[i] += (feature_component - self.means[i]) ** 2
        for i in range(num_features):
            self.stds[i] = math.sqrt(self.stds[i] / len(self.initial_features))

    def standardize_feature(self, feature: Feature) -> List[float]:
        standardized_feature = []
        for i, feature_component in enumerate(feature.get_vector()):
            standardized_feature.append(
                (feature_component - self.means[i]) / self.stds[i]
            )
        return standardized_feature
