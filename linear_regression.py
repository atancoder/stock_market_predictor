from typing import Any, List, Optional

import numpy as np
from sklearn.linear_model import LinearRegression

from feature_set import Feature, LabeledData, Standardizer


class LinearRegressionModel:
    def __init__(self, training_data: List[LabeledData]) -> None:
        self.training_data = training_data
        self.standardizer = Standardizer([data.feature for data in training_data])
        self.model: Optional[LinearRegression] = None

    def train(self) -> None:
        standardized_features = [
            self.standardizer.standardize_feature(data.feature)
            for data in self.training_data
        ]
        labels = [data.label for data in self.training_data]
        self.model = LinearRegression().fit(standardized_features, labels)
        import pdb

        pdb.set_trace()

    def predict(self, feature: Feature) -> Any:
        assert self.model is not None, "Must train model before predicting"
        standardized_feature = self.standardizer.standardize_feature(feature)
        return self.model.predict(np.array([standardized_feature]))[0]

    def score(self, test_data: List[LabeledData]) -> Any:
        assert self.model is not None, "Must train model before predicting"
        standardized_features = [
            self.standardizer.standardize_feature(data.feature) for data in test_data
        ]
        labels = [data.label for data in test_data]
        return self.model.score(standardized_features, labels)
