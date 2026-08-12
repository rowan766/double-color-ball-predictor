def red_hit_count(predicted: list[int], actual: list[int]) -> int:
    return len(set(predicted) & set(actual))


def blue_hit(predicted: int, actual: int) -> bool:
    return predicted == actual
