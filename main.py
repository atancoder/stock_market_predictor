import random
from datetime import date
from typing import List, Tuple

from alpha_vantage_api import AlphaVantageAPI
from data_fetcher import DataFetcher, split_data
from feature_set import LabeledData
from linear_regression import LinearRegressionModel
from symbols import SYMBOLS

DATE = date(2015, 12, 31)
TWO_YEARS_LATER = date(2017, 12, 31)


def save_to_csv(labeled_data: List[LabeledData]) -> None:
    with open("labeled_data.csv", "w") as f:
        f.write("pe_ratio, market_cap, past_pct_change,label\n")
        for data in labeled_data:
            f.write(
                f"{data.feature.pe_ratio}, {data.feature.market_cap}, {data.feature.past_pct_change},{data.label}\n"
            )


def main() -> None:
    # Fetch data
    data_fetcher = DataFetcher(
        AlphaVantageAPI(), curr_date=DATE, predictor_date=TWO_YEARS_LATER
    )
    data_fetcher.populate_stock_data(SYMBOLS)
    save_to_csv(data_fetcher.get_labeled_data())

    # training_set, test_set, validation_set = split_data(data_fetcher.get_labeled_data())

    # # Train
    # model = LinearRegressionModel(training_set)
    # model.train()

    # # Score
    # training_score = model.score(training_set)
    # test_score = model.score(test_set)
    # print("Training score: {}".format(training_score))
    # print("Test score: {}".format(test_score))


if __name__ == "__main__":
    main()
