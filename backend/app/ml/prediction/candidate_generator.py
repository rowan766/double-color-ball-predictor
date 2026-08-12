import random

from app.schemas.prediction import CandidateNumbers


class CandidateGenerator:
    def __init__(self, strategy: str = "top_k", seed: int = 42):
        self.strategy = strategy
        self.random = random.Random(seed)

    def generate(
        self,
        red_probabilities: dict[int, float],
        blue_probabilities: dict[int, float],
        count: int = 5,
    ) -> list[CandidateNumbers]:
        if self.strategy == "top_k":
            return [self._top_k(red_probabilities, blue_probabilities)]
        if self.strategy == "weighted_sample":
            return [
                self._weighted_sample(red_probabilities, blue_probabilities, locked_reds=[])
                for _ in range(count)
            ]
        if self.strategy == "mixed":
            top_reds = [
                number
                for number, _ in sorted(red_probabilities.items(), key=lambda item: item[1], reverse=True)[:3]
            ]
            return [
                self._top_k(red_probabilities, blue_probabilities),
                *[
                    self._weighted_sample(red_probabilities, blue_probabilities, locked_reds=top_reds)
                    for _ in range(max(count - 1, 0))
                ],
            ][:count]
        raise ValueError(f"Unsupported candidate strategy: {self.strategy}")

    def _top_k(
        self,
        red_probabilities: dict[int, float],
        blue_probabilities: dict[int, float],
    ) -> CandidateNumbers:
        red_numbers = sorted(self._top_numbers(red_probabilities, 6))
        blue_number = self._top_numbers(blue_probabilities, 1)[0]
        return CandidateNumbers(
            red_numbers=red_numbers,
            blue_number=blue_number,
            score=self._score(red_numbers, blue_number, red_probabilities, blue_probabilities),
        )

    def _weighted_sample(
        self,
        red_probabilities: dict[int, float],
        blue_probabilities: dict[int, float],
        locked_reds: list[int],
    ) -> CandidateNumbers:
        selected = set(locked_reds)
        pool = [number for number in sorted(red_probabilities) if number not in selected]
        while len(selected) < 6:
            weights = [max(red_probabilities[number], 0.0001) for number in pool]
            chosen = self.random.choices(pool, weights=weights, k=1)[0]
            selected.add(chosen)
            pool.remove(chosen)
        blue_pool = sorted(blue_probabilities)
        blue_number = self.random.choices(
            blue_pool,
            weights=[max(blue_probabilities[number], 0.0001) for number in blue_pool],
            k=1,
        )[0]
        red_numbers = sorted(selected)
        return CandidateNumbers(
            red_numbers=red_numbers,
            blue_number=blue_number,
            score=self._score(red_numbers, blue_number, red_probabilities, blue_probabilities),
        )

    def _top_numbers(self, probabilities: dict[int, float], count: int) -> list[int]:
        return [
            number
            for number, _ in sorted(
                probabilities.items(), key=lambda item: (-item[1], item[0])
            )[:count]
        ]

    def _score(
        self,
        red_numbers: list[int],
        blue_number: int,
        red_probabilities: dict[int, float],
        blue_probabilities: dict[int, float],
    ) -> float:
        return sum(red_probabilities[number] for number in red_numbers) + blue_probabilities[blue_number]
