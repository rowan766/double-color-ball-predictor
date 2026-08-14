import random
from itertools import combinations

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
        if self.strategy == "optimized":
            return self._optimized(red_probabilities, blue_probabilities, count=count)
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

    def _optimized(
        self,
        red_probabilities: dict[int, float],
        blue_probabilities: dict[int, float],
        count: int,
    ) -> list[CandidateNumbers]:
        red_pool = self._top_numbers(red_probabilities, 15)
        blue_pool = self._top_numbers(blue_probabilities, 3)
        candidates: list[CandidateNumbers] = []
        seen: set[tuple[tuple[int, ...], int]] = set()

        for reds in combinations(sorted(red_pool), 6):
            if not self._passes_structure_filters(list(reds)):
                continue
            for blue_number in blue_pool:
                self._append_unique_candidate(
                    candidates,
                    seen,
                    list(reds),
                    blue_number,
                    red_probabilities,
                    blue_probabilities,
                )

        for _ in range(max(count * 60, 300)):
            sample = self._weighted_sample(red_probabilities, blue_probabilities, locked_reds=[])
            if self._passes_structure_filters(sample.red_numbers):
                self._append_unique_candidate(
                    candidates,
                    seen,
                    sample.red_numbers,
                    sample.blue_number,
                    red_probabilities,
                    blue_probabilities,
                )

        ranked = sorted(
            candidates,
            key=lambda candidate: (
                candidate.score or 0,
                -sum(candidate.red_numbers),
                -candidate.blue_number,
            ),
            reverse=True,
        )
        if not ranked:
            return [
                self._weighted_sample(red_probabilities, blue_probabilities, locked_reds=[])
                for _ in range(count)
            ]
        return ranked[:count]

    def _append_unique_candidate(
        self,
        candidates: list[CandidateNumbers],
        seen: set[tuple[tuple[int, ...], int]],
        red_numbers: list[int],
        blue_number: int,
        red_probabilities: dict[int, float],
        blue_probabilities: dict[int, float],
    ) -> None:
        normalized_reds = sorted(red_numbers)
        key = (tuple(normalized_reds), blue_number)
        if key in seen:
            return
        seen.add(key)
        candidates.append(
            CandidateNumbers(
                red_numbers=normalized_reds,
                blue_number=blue_number,
                score=self._score(normalized_reds, blue_number, red_probabilities, blue_probabilities)
                + self._structure_score(normalized_reds),
            )
        )

    def _passes_structure_filters(self, red_numbers: list[int]) -> bool:
        total = sum(red_numbers)
        if total < 65 or total > 145:
            return False
        odd_count = sum(1 for number in red_numbers if number % 2 == 1)
        if odd_count < 2 or odd_count > 4:
            return False
        big_count = sum(1 for number in red_numbers if number >= 17)
        if big_count < 2 or big_count > 4:
            return False
        zones = [
            sum(1 for number in red_numbers if 1 <= number <= 11),
            sum(1 for number in red_numbers if 12 <= number <= 22),
            sum(1 for number in red_numbers if 23 <= number <= 33),
        ]
        if min(zones) == 0 or max(zones) > 3:
            return False
        if self._max_consecutive_run(red_numbers) > 2:
            return False
        return red_numbers[-1] - red_numbers[0] >= 12

    def _structure_score(self, red_numbers: list[int]) -> float:
        total = sum(red_numbers)
        odd_count = sum(1 for number in red_numbers if number % 2 == 1)
        big_count = sum(1 for number in red_numbers if number >= 17)
        zones = [
            sum(1 for number in red_numbers if 1 <= number <= 11),
            sum(1 for number in red_numbers if 12 <= number <= 22),
            sum(1 for number in red_numbers if 23 <= number <= 33),
        ]
        score = 0.0
        score += max(0.0, 1 - abs(total - 102) / 50) * 0.18
        score += (1 - abs(odd_count - 3) / 3) * 0.12
        score += (1 - abs(big_count - 3) / 3) * 0.12
        score += (1 - (max(zones) - min(zones)) / 4) * 0.12
        score += max(0.0, 1 - self._max_gap(red_numbers) / 18) * 0.08
        score -= max(0, self._max_consecutive_run(red_numbers) - 1) * 0.04
        return score

    def _max_consecutive_run(self, red_numbers: list[int]) -> int:
        longest = 1
        current = 1
        for previous, number in zip(red_numbers, red_numbers[1:]):
            if number == previous + 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        return longest

    def _max_gap(self, red_numbers: list[int]) -> int:
        return max(number - previous for previous, number in zip(red_numbers, red_numbers[1:]))

    def _score(
        self,
        red_numbers: list[int],
        blue_number: int,
        red_probabilities: dict[int, float],
        blue_probabilities: dict[int, float],
    ) -> float:
        return sum(red_probabilities[number] for number in red_numbers) + blue_probabilities[blue_number]
