from app.ml.constants import BLUE_NUMBERS, RED_NUMBERS
from app.ml.datasets.dataset_builder import DatasetBuilder
from app.ml.features.feature_pipeline import FeaturePipeline
from app.ml.models.statistical_model import StatisticalModel


class OptionalBinaryClassifierModel(StatisticalModel):
    classifier_kind = "sklearn_logistic"

    def fit(self, train_draws: list) -> None:
        super().fit(train_draws)
        self.dataset_builder = DatasetBuilder()
        self.red_classifier = None
        self.blue_classifier = None
        self._fit_optional_classifiers(train_draws)

    def predict_red_probabilities(self, features=None) -> dict[int, float]:
        if self.red_classifier is None:
            return super().predict_red_probabilities(features)
        pipeline = FeaturePipeline()
        rows = self._rows_from_feature_map(pipeline.transform_red(self.train_draws))
        probabilities = self._predict_positive_probabilities(self.red_classifier, rows, RED_NUMBERS)
        return self._normalize_to_expected_count(probabilities, expected_count=6)

    def predict_blue_probabilities(self, features=None) -> dict[int, float]:
        if self.blue_classifier is None:
            return super().predict_blue_probabilities(features)
        pipeline = FeaturePipeline()
        rows = self._rows_from_feature_map(pipeline.transform_blue(self.train_draws))
        probabilities = self._predict_positive_probabilities(self.blue_classifier, rows, BLUE_NUMBERS)
        return self._normalize_to_expected_count(probabilities, expected_count=1)

    def _fit_optional_classifiers(self, train_draws: list) -> None:
        red_rows, red_labels = self.dataset_builder.build_red_dataset(train_draws)
        blue_rows, blue_labels = self.dataset_builder.build_blue_dataset(train_draws)
        self.red_classifier = self._fit_one(red_rows, red_labels)
        self.blue_classifier = self._fit_one(blue_rows, blue_labels)

    def _fit_one(self, rows: list[list[float]], labels: list[int]):
        if not rows or len(set(labels)) < 2:
            return None
        classifier = self._create_classifier()
        if classifier is None:
            return None
        try:
            classifier.fit(rows, labels)
            return classifier
        except Exception:
            return None

    def _create_classifier(self):
        try:
            if self.classifier_kind == "sklearn_logistic":
                from sklearn.linear_model import LogisticRegression

                return LogisticRegression(max_iter=500, class_weight="balanced")
            if self.classifier_kind == "lightgbm":
                from lightgbm import LGBMClassifier

                return LGBMClassifier(n_estimators=80, learning_rate=0.05, random_state=42, verbose=-1)
            if self.classifier_kind == "xgboost":
                from xgboost import XGBClassifier

                return XGBClassifier(
                    n_estimators=80,
                    learning_rate=0.05,
                    max_depth=3,
                    random_state=42,
                    eval_metric="logloss",
                )
        except Exception:
            return None
        return None

    def _rows_from_feature_map(self, feature_map: dict[int, dict[str, float]]) -> list[list[float]]:
        from app.ml.features.feature_pipeline import FEATURE_COLUMNS

        return [[features[column] for column in FEATURE_COLUMNS] for _, features in sorted(feature_map.items())]

    def _predict_positive_probabilities(self, classifier, rows: list[list[float]], numbers) -> dict[int, float]:
        raw = classifier.predict_proba(rows)
        return {number: float(raw[index][1]) for index, number in enumerate(numbers)}
