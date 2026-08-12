from collections import Counter

from app.ml.constants import BLUE_NUMBERS, RED_NUMBERS


class NumberFeatureBuilder:
    windows = (5, 10, 20, 50, 100)

    def build_empty_red_features(self) -> dict[int, dict[str, float]]:
        return {number: {f"count_last_{window}": 0.0 for window in self.windows} for number in RED_NUMBERS}

    def build_empty_blue_features(self) -> dict[int, dict[str, float]]:
        return {number: {f"count_last_{window}": 0.0 for window in self.windows} for number in BLUE_NUMBERS}

    def build_red_features(self, history_draws: list) -> dict[int, dict[str, float]]:
        return {
            number: self._build_number_features(
                history_draws=history_draws,
                number=number,
                number_getter=lambda draw: draw.red_numbers,
            )
            for number in RED_NUMBERS
        }

    def build_blue_features(self, history_draws: list) -> dict[int, dict[str, float]]:
        return {
            number: self._build_number_features(
                history_draws=history_draws,
                number=number,
                number_getter=lambda draw: [draw.blue_number],
            )
            for number in BLUE_NUMBERS
        }

    def _build_number_features(
        self,
        history_draws: list,
        number: int,
        number_getter,
    ) -> dict[str, float]:
        features: dict[str, float] = {"number": float(number)}
        appearances: list[int] = []
        gaps: list[int] = []
        current_gap = 0
        last_seen_distance = len(history_draws) + 1

        for index, draw in enumerate(history_draws):
            appeared = number in number_getter(draw)
            appearances.append(1 if appeared else 0)
            if appeared:
                if current_gap > 0:
                    gaps.append(current_gap)
                current_gap = 0
                last_seen_distance = len(history_draws) - index
            else:
                current_gap += 1

        for window in self.windows:
            features[f"count_last_{window}"] = float(sum(appearances[-window:]))
            features[f"freq_last_{window}"] = features[f"count_last_{window}"] / window

        total_draws = max(len(history_draws), 1)
        total_appearances = sum(appearances)
        features["current_omission"] = float(current_gap)
        features["avg_omission"] = float(sum(gaps) / len(gaps)) if gaps else float(total_draws)
        features["max_omission"] = float(max(gaps)) if gaps else float(current_gap)
        features["historical_frequency"] = total_appearances / total_draws
        features["last_seen_distance"] = float(last_seen_distance)
        return features


def count_red_frequency(draws: list) -> Counter[int]:
    counter: Counter[int] = Counter()
    for draw in draws:
        counter.update(draw.red_numbers)
    return counter


def count_blue_frequency(draws: list) -> Counter[int]:
    counter: Counter[int] = Counter()
    for draw in draws:
        counter.update([draw.blue_number])
    return counter
