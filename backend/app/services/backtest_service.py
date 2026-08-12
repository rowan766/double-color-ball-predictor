from collections import Counter

from sqlalchemy.orm import Session

from app.ml.backtesting.evaluator import BacktestEvaluator
from app.ml.models.registry import create_model
from app.ml.prediction.candidate_generator import CandidateGenerator
from app.repositories.backtest_repository import BacktestRepository
from app.repositories.draw_repository import DrawRepository
from app.repositories.model_repository import ModelRepository
from app.schemas.backtest import BacktestMetricRead, BacktestRunRequest


class BacktestService:
    def __init__(self, db: Session):
        self.draw_repository = DrawRepository(db)
        self.model_repository = ModelRepository(db)
        self.backtest_repository = BacktestRepository(db)
        self.evaluator = BacktestEvaluator()

    def run_backtest(self, request: BacktestRunRequest) -> list[BacktestMetricRead]:
        target_draws = self.draw_repository.list_issue_range(request.start_issue_no, request.end_issue_no)
        if not target_draws:
            raise ValueError("No target draws found for backtest range")

        metrics = [self._run_model_backtest(model_key, target_draws, request) for model_key in request.model_keys]
        baseline = next((metric for metric in metrics if metric.model_key == "random_baseline"), None)
        if baseline is not None:
            for metric in metrics:
                metric.random_baseline_diff = {
                    "avg_red_hits": metric.avg_red_hits - baseline.avg_red_hits,
                    "blue_hit_rate": metric.blue_hit_rate - baseline.blue_hit_rate,
                    "ranking_score": metric.ranking_score - baseline.ranking_score,
                }
        self.backtest_repository.commit()
        return metrics

    def leaderboard(self) -> list[BacktestMetricRead]:
        return [
            BacktestMetricRead(
                model_key=model.model_key,
                backtest_run_id=metric.backtest_run_id,
                total_predictions=metric.total_predictions,
                avg_red_hits=metric.avg_red_hits,
                blue_hit_rate=metric.blue_hit_rate,
                red_hit_distribution=metric.red_hit_distribution,
                prize_distribution=metric.prize_distribution,
                random_baseline_diff=metric.random_baseline_diff,
                ranking_score=metric.ranking_score,
            )
            for metric, model in self.backtest_repository.leaderboard()
        ]

    def _run_model_backtest(
        self,
        model_key: str,
        target_draws: list,
        request: BacktestRunRequest,
    ) -> BacktestMetricRead:
        db_model = self.model_repository.get_or_create_by_key(model_key)
        run = self.backtest_repository.create_run(
            name=f"{request.name} - {model_key}",
            model_id=db_model.id,
            start_issue_no=request.start_issue_no,
            end_issue_no=request.end_issue_no,
            initial_train_size=request.initial_train_size,
            candidate_strategy=request.candidate_strategy,
            config=request.model_dump(),
        )
        red_hits: list[int] = []
        blue_hits: list[bool] = []
        prize_counter: Counter[str] = Counter()

        for index, target_draw in enumerate(target_draws):
            train_draws = self.draw_repository.list_until_issue(target_draw.issue_no, inclusive=False)
            if len(train_draws) < request.initial_train_size:
                continue
            model = create_model(model_key)
            model.fit(train_draws)
            red_probabilities = model.predict_red_probabilities(features=None)
            blue_probabilities = model.predict_blue_probabilities(features=None)
            candidate = CandidateGenerator(
                strategy=request.candidate_strategy,
                seed=42 + index,
            ).generate(red_probabilities, blue_probabilities, count=1)[0]
            evaluation = self.evaluator.evaluate_one(
                predicted_reds=candidate.red_numbers,
                predicted_blue=candidate.blue_number,
                actual_reds=target_draw.red_numbers,
                actual_blue=target_draw.blue_number,
            )
            red_hits.append(evaluation["red_hit_count"])
            blue_hits.append(evaluation["blue_hit"])
            if evaluation["prize_level"] is not None:
                prize_counter.update([evaluation["prize_level"]])
            self.backtest_repository.create_result(
                backtest_run_id=run.id,
                model_id=db_model.id,
                target_issue_no=target_draw.issue_no,
                train_until_issue_no=train_draws[-1].issue_no,
                predicted_red_numbers=candidate.red_numbers,
                predicted_blue_number=candidate.blue_number,
                actual_red_numbers=target_draw.red_numbers,
                actual_blue_number=target_draw.blue_number,
                red_hit_count=evaluation["red_hit_count"],
                blue_hit=evaluation["blue_hit"],
                prize_level=evaluation["prize_level"],
                red_probabilities={str(k): v for k, v in red_probabilities.items()},
                blue_probabilities={str(k): v for k, v in blue_probabilities.items()},
            )

        total = len(red_hits)
        distribution = Counter(red_hits)
        avg_red_hits = sum(red_hits) / total if total else 0.0
        blue_hit_rate = sum(1 for hit in blue_hits if hit) / total if total else 0.0
        ranking_score = avg_red_hits + blue_hit_rate
        metric = self.backtest_repository.create_metric(
            model_id=db_model.id,
            backtest_run_id=run.id,
            total_predictions=total,
            avg_red_hits=avg_red_hits,
            blue_hit_rate=blue_hit_rate,
            red_hit_distribution={
                str(hit_count): distribution.get(hit_count, 0) / total if total else 0.0
                for hit_count in range(7)
            },
            prize_distribution=dict(prize_counter),
            random_baseline_diff={},
            ranking_score=ranking_score,
        )
        return BacktestMetricRead(
            model_key=model_key,
            backtest_run_id=metric.backtest_run_id,
            total_predictions=total,
            avg_red_hits=avg_red_hits,
            blue_hit_rate=blue_hit_rate,
            red_hit_distribution={
                str(hit_count): distribution.get(hit_count, 0) / total if total else 0.0
                for hit_count in range(7)
            },
            prize_distribution=dict(prize_counter),
            ranking_score=ranking_score,
        )
