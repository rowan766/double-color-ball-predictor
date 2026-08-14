from app.ml.constants import BLUE_NUMBERS, RED_NUMBERS
from app.ml.models.base import BaseLotteryModel
from app.ml.models.lightgbm_model import LightGBMLotteryModel
from app.ml.models.logistic_regression_model import LogisticRegressionLotteryModel
from app.ml.models.statistical_model import StatisticalModel
from app.ml.models.xgboost_model import XGBoostLotteryModel


class OptimizedEnsembleModel(BaseLotteryModel):
    model_key = "optimized_ensemble"
    display_name = "Optimized Ensemble"
    model_type = "ensemble"

    red_weights = {
        "statistical": 0.45,
        "logistic_regression": 0.20,
        "lightgbm": 0.20,
        "xgboost": 0.15,
    }
    blue_weights = {
        "statistical": 0.30,
        "logistic_regression": 0.20,
        "lightgbm": 0.25,
        "xgboost": 0.25,
    }

    def fit(self, train_draws: list) -> None:
        super().fit(train_draws)
        self.models = {
            "statistical": StatisticalModel(),
            "logistic_regression": LogisticRegressionLotteryModel(),
            "lightgbm": LightGBMLotteryModel(),
            "xgboost": XGBoostLotteryModel(),
        }
        for model in self.models.values():
            model.fit(train_draws)

    def predict_red_probabilities(self, features=None) -> dict[int, float]:
        probability_sets = {
            key: model.predict_red_probabilities(features)
            for key, model in self.models.items()
        }
        blended = self._blend(probability_sets, self.red_weights, RED_NUMBERS)
        return self._stabilize(blended, base_probability=6 / 33, expected_count=6)

    def predict_blue_probabilities(self, features=None) -> dict[int, float]:
        probability_sets = {
            key: model.predict_blue_probabilities(features)
            for key, model in self.models.items()
        }
        blended = self._blend(probability_sets, self.blue_weights, BLUE_NUMBERS)
        return self._stabilize(blended, base_probability=1 / 16, expected_count=1)

    def _blend(
        self,
        probability_sets: dict[str, dict[int, float]],
        weights: dict[str, float],
        numbers,
    ) -> dict[int, float]:
        total_weight = sum(weights.values()) or 1
        return {
            number: sum(
                probability_sets[key].get(number, 0.0) * weight
                for key, weight in weights.items()
            )
            / total_weight
            for number in numbers
        }

    def _stabilize(
        self,
        probabilities: dict[int, float],
        base_probability: float,
        expected_count: float,
    ) -> dict[int, float]:
        stabilized = {
            number: probability * 0.85 + base_probability * 0.15
            for number, probability in probabilities.items()
        }
        return self._normalize_to_expected_count(stabilized, expected_count)

    def _normalize_to_expected_count(
        self,
        probabilities: dict[int, float],
        expected_count: float,
    ) -> dict[int, float]:
        total = sum(probabilities.values()) or 1
        return {
            number: min(max(probability / total * expected_count, 0.0001), 0.9999)
            for number, probability in probabilities.items()
        }
