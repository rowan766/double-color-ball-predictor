from app.ml.backtesting.evaluator import BacktestEvaluator
from app.ml.backtesting.metrics import blue_hit, red_hit_count


def test_hit_metrics():
    assert red_hit_count([1, 2, 3, 4, 5, 6], [1, 2, 8, 9, 10, 11]) == 2
    assert blue_hit(8, 8) is True
    assert blue_hit(8, 9) is False


def test_prize_level():
    evaluator = BacktestEvaluator()
    assert evaluator.prize_level(6, True) == "first"
    assert evaluator.prize_level(6, False) == "second"
    assert evaluator.prize_level(0, True) == "sixth"
    assert evaluator.prize_level(0, False) is None
