from typing import Any, List, Optional

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from feature_set import Feature, LabeledData


class LinearRegressionModel:
    def __init__(self, training_data: List[LabeledData]) -> None:
        self.training_data = training_data
        self.pipeline = Pipeline(
            [("scaler", StandardScaler()), ("lr", LinearRegression())]
        )

    def train(self) -> None:
        features = [data.feature.get_vector() for data in self.training_data]
        labels = [data.label for data in self.training_data]
        self.pipeline.fit(features, labels)

    def predict(self, feature: Feature) -> Any:
        return self.pipeline.predict([feature])[0]

    def score(self, test_data: List[LabeledData]) -> Any:
        features = [data.feature.get_vector() for data in test_data]
        labels = [data.label for data in test_data]
        return self.pipeline.score(features, labels)
