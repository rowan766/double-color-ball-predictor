from app.ml.constants import BLUE_NUMBERS, RED_NUMBERS
from app.ml.prediction.candidate_generator import CandidateGenerator


def test_top_k_candidate_generator():
    reds = {number: float(number) for number in RED_NUMBERS}
    blues = {number: float(number) for number in BLUE_NUMBERS}

    candidates = CandidateGenerator().generate(reds, blues, count=5)

    assert len(candidates) == 1
    assert candidates[0].red_numbers == [28, 29, 30, 31, 32, 33]
    assert candidates[0].blue_number == 16


def test_weighted_sample_candidate_generator_shape():
    reds = {number: 1.0 for number in RED_NUMBERS}
    blues = {number: 1.0 for number in BLUE_NUMBERS}

    candidates = CandidateGenerator(strategy="weighted_sample", seed=1).generate(reds, blues, count=3)

    assert len(candidates) == 3
    assert all(len(candidate.red_numbers) == 6 for candidate in candidates)
    assert all(1 <= candidate.blue_number <= 16 for candidate in candidates)
