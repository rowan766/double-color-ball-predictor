from app.ml.features.draw_features import calculate_draw_features


def test_calculate_draw_features():
    features = calculate_draw_features([1, 2, 3, 16, 17, 33], previous_red_numbers=[1, 4, 6, 8, 10, 12])

    assert features["red_sum"] == 72
    assert features["red_span"] == 32
    assert features["odd_count"] == 4
    assert features["even_count"] == 2
    assert features["repeat_with_prev_count"] == 1
    assert features["prime_count"] == 2
