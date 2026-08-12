from app.ml.constants import BLUE_NUMBERS, RED_NUMBERS
from app.ml.models.base import BaseLotteryModel


class RandomBaselineModel(BaseLotteryModel):
    model_key = "random_baseline"
    display_name = "Random Baseline"
    model_type = "baseline"

    def predict_red_probabilities(self, features) -> dict[int, float]:
        return {number: 6 / 33 for number in RED_NUMBERS}

    def predict_blue_probabilities(self, features) -> dict[int, float]:
        return {number: 1 / 16 for number in BLUE_NUMBERS}
