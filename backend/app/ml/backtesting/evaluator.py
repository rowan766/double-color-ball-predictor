from app.ml.backtesting.metrics import blue_hit, red_hit_count


class BacktestEvaluator:
    def evaluate_one(self, predicted_reds: list[int], predicted_blue: int, actual_reds: list[int], actual_blue: int):
        red_hits = red_hit_count(predicted_reds, actual_reds)
        return {
            "red_hit_count": red_hits,
            "blue_hit": blue_hit(predicted_blue, actual_blue),
            "prize_level": self.prize_level(red_hits, predicted_blue == actual_blue),
        }

    def prize_level(self, red_hits: int, is_blue_hit: bool) -> str | None:
        if red_hits == 6 and is_blue_hit:
            return "first"
        if red_hits == 6:
            return "second"
        if red_hits == 5 and is_blue_hit:
            return "third"
        if red_hits == 5 or (red_hits == 4 and is_blue_hit):
            return "fourth"
        if red_hits == 4 or (red_hits == 3 and is_blue_hit):
            return "fifth"
        if is_blue_hit:
            return "sixth"
        return None
