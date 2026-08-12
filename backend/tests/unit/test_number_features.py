from types import SimpleNamespace

from app.ml.features.number_features import NumberFeatureBuilder


def test_number_features_use_history_only():
    draws = [
        SimpleNamespace(red_numbers=[1, 2, 3, 4, 5, 6], blue_number=1),
        SimpleNamespace(red_numbers=[1, 7, 8, 9, 10, 11], blue_number=2),
        SimpleNamespace(red_numbers=[12, 13, 14, 15, 16, 17], blue_number=1),
    ]

    red_features = NumberFeatureBuilder().build_red_features(draws)
    blue_features = NumberFeatureBuilder().build_blue_features(draws)

    assert red_features[1]["count_last_5"] == 2
    assert red_features[1]["current_omission"] == 1
    assert blue_features[1]["count_last_5"] == 2

