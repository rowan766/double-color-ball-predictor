class TrendFeatureBuilder:
    def build(self, number_features: dict[int, dict[str, float]]) -> dict[int, dict[str, float]]:
        for features in number_features.values():
            features["freq_5_vs_20"] = features.get("freq_last_5", 0.0) - features.get(
                "freq_last_20", 0.0
            )
            features["freq_10_vs_50"] = features.get("freq_last_10", 0.0) - features.get(
                "freq_last_50", 0.0
            )
            features["short_vs_long"] = features.get("freq_last_20", 0.0) - features.get(
                "freq_last_100", 0.0
            )
        return number_features
