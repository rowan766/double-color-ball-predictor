from app.ml.features.number_features import NumberFeatureBuilder
from app.ml.features.trend_features import TrendFeatureBuilder


FEATURE_COLUMNS = [
    "number",
    "count_last_5",
    "freq_last_5",
    "count_last_10",
    "freq_last_10",
    "count_last_20",
    "freq_last_20",
    "count_last_50",
    "freq_last_50",
    "count_last_100",
    "freq_last_100",
    "current_omission",
    "avg_omission",
    "max_omission",
    "historical_frequency",
    "last_seen_distance",
    "freq_5_vs_20",
    "freq_10_vs_50",
    "short_vs_long",
]


class FeaturePipeline:
    def __init__(self):
        self.number_builder = NumberFeatureBuilder()
        self.trend_builder = TrendFeatureBuilder()

    def transform_red(self, history_draws: list) -> dict[int, dict[str, float]]:
        features = self.number_builder.build_red_features(history_draws)
        return self.trend_builder.build(features)

    def transform_blue(self, history_draws: list) -> dict[int, dict[str, float]]:
        features = self.number_builder.build_blue_features(history_draws)
        return self.trend_builder.build(features)


def vectorize_feature_map(feature_map: dict[int, dict[str, float]]) -> list[list[float]]:
    return [[features[column] for column in FEATURE_COLUMNS] for _, features in sorted(feature_map.items())]
