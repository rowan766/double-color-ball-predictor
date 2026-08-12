def normalize_probabilities(probabilities: dict[int, float]) -> dict[int, float]:
    total = sum(probabilities.values())
    if total <= 0:
        return probabilities
    return {number: value / total for number, value in probabilities.items()}
