from app.ml.constants import BLUE_NUMBERS, RED_NUMBERS
from app.ml.features.feature_pipeline import FEATURE_COLUMNS, FeaturePipeline


class DatasetBuilder:
    def __init__(self, min_history_size: int = 5):
        self.min_history_size = min_history_size
        self.pipeline = FeaturePipeline()

    def build_red_dataset(self, draws: list):
        rows: list[list[float]] = []
        labels: list[int] = []
        for target_index in range(self.min_history_size, len(draws)):
            history = draws[:target_index]
            target_reds = set(draws[target_index].red_numbers)
            features = self.pipeline.transform_red(history)
            for number in RED_NUMBERS:
                rows.append([features[number][column] for column in FEATURE_COLUMNS])
                labels.append(1 if number in target_reds else 0)
        return rows, labels

    def build_blue_dataset(self, draws: list):
        rows: list[list[float]] = []
        labels: list[int] = []
        for target_index in range(self.min_history_size, len(draws)):
            history = draws[:target_index]
            target_blue = draws[target_index].blue_number
            features = self.pipeline.transform_blue(history)
            for number in BLUE_NUMBERS:
                rows.append([features[number][column] for column in FEATURE_COLUMNS])
                labels.append(1 if number == target_blue else 0)
        return rows, labels
