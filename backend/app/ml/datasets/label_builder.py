class LabelBuilder:
    def build_red_labels(self, target_draw, numbers=range(1, 34)) -> list[int]:
        target_reds = set(target_draw.red_numbers)
        return [1 if number in target_reds else 0 for number in numbers]

    def build_blue_labels(self, target_draw, numbers=range(1, 17)) -> list[int]:
        return [1 if number == target_draw.blue_number else 0 for number in numbers]
