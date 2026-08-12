from app.ml.constants import BLUE_NUMBERS, RED_NUMBERS
from app.ml.features.feature_pipeline import FeaturePipeline
from app.ml.models.base import BaseLotteryModel


class StatisticalModel(BaseLotteryModel):
    model_key = "statistical"
    display_name = "Statistical Model"
    model_type = "statistical"

    def fit(self, train_draws: list) -> None:
        super().fit(train_draws)
        self.pipeline = FeaturePipeline()

    def predict_red_probabilities(self, features=None) -> dict[int, float]:
        feature_map = self.pipeline.transform_red(self.train_draws)
        scores = {
            number: self._score_number(feature_map[number], base_probability=6 / 33)
            for number in RED_NUMBERS
        }
        return self._normalize_to_expected_count(scores, expected_count=6)

    def predict_blue_probabilities(self, features=None) -> dict[int, float]:
        feature_map = self.pipeline.transform_blue(self.train_draws)
        scores = {
            number: self._score_number(feature_map[number], base_probability=1 / 16)
            for number in BLUE_NUMBERS
        }
        return self._normalize_to_expected_count(scores, expected_count=1)

    def _score_number(self, features: dict[str, float], base_probability: float) -> float:
        score = (
            base_probability
            + features["historical_frequency"] * 1.5
            + features["freq_last_20"] * 0.8
            + features["freq_5_vs_20"] * 0.5
            + features["short_vs_long"] * 0.3
        )
        omission_penalty = min(features["current_omission"] / 200, 0.1)
        return max(score - omission_penalty, 0.0001)

    def _normalize_to_expected_count(
        self, scores: dict[int, float], expected_count: float
    ) -> dict[int, float]:
        total = sum(scores.values()) or 1
        probabilities = {
            number: min(max(score / total * expected_count, 0.0001), 0.9999)
            for number, score in scores.items()
        }
        return probabilities
