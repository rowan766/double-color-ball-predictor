from app.ml.backtesting.evaluator import BacktestEvaluator
from app.ml.prediction.candidate_generator import CandidateGenerator


class BacktestRunner:
    def __init__(self, candidate_strategy: str = "top_k"):
        self.candidate_strategy = candidate_strategy
        self.evaluator = BacktestEvaluator()

    def run(self, draws: list, model_factory, initial_train_size: int) -> list[dict]:
        results: list[dict] = []
        for target_index in range(initial_train_size, len(draws)):
            train_draws = draws[:target_index]
            target_draw = draws[target_index]
            model = model_factory()
            model.fit(train_draws)
            red_probabilities = model.predict_red_probabilities(None)
            blue_probabilities = model.predict_blue_probabilities(None)
            candidate = CandidateGenerator(
                strategy=self.candidate_strategy,
                seed=42 + target_index,
            ).generate(red_probabilities, blue_probabilities, count=1)[0]
            evaluation = self.evaluator.evaluate_one(
                predicted_reds=candidate.red_numbers,
                predicted_blue=candidate.blue_number,
                actual_reds=target_draw.red_numbers,
                actual_blue=target_draw.blue_number,
            )
            results.append(
                {
                    "target_issue_no": target_draw.issue_no,
                    "train_until_issue_no": train_draws[-1].issue_no,
                    "candidate": candidate,
                    "red_probabilities": red_probabilities,
                    "blue_probabilities": blue_probabilities,
                    **evaluation,
                }
            )
        return results
