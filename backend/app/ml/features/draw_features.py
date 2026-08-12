PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}


def calculate_draw_features(red_numbers: list[int], previous_red_numbers: list[int] | None = None) -> dict:
    sorted_reds = sorted(red_numbers)
    previous = set(previous_red_numbers or [])
    return {
        "red_sum": sum(sorted_reds),
        "red_span": sorted_reds[-1] - sorted_reds[0],
        "odd_count": sum(1 for number in sorted_reds if number % 2 == 1),
        "even_count": sum(1 for number in sorted_reds if number % 2 == 0),
        "big_count": sum(1 for number in sorted_reds if number >= 17),
        "small_count": sum(1 for number in sorted_reds if number <= 16),
        "zone_1_count": sum(1 for number in sorted_reds if 1 <= number <= 11),
        "zone_2_count": sum(1 for number in sorted_reds if 12 <= number <= 22),
        "zone_3_count": sum(1 for number in sorted_reds if 23 <= number <= 33),
        "consecutive_count": sum(
            1 for left, right in zip(sorted_reds, sorted_reds[1:]) if right - left == 1
        ),
        "repeat_with_prev_count": len(set(sorted_reds) & previous),
        "prime_count": sum(1 for number in sorted_reds if number in PRIMES),
    }
