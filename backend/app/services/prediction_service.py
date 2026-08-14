from datetime import datetime, timedelta, timezone

from app.ml.models.registry import create_model
from app.ml.prediction.candidate_generator import CandidateGenerator
from app.db.models.draw import LotteryDraw
from app.repositories.draw_repository import DrawRepository
from app.repositories.model_repository import ModelRepository
from app.repositories.prediction_repository import PredictionRepository
from app.schemas.prediction import ModelPredictionRead, PredictionRunRequest
from sqlalchemy.orm import Session

DEFAULT_AUTO_MODEL_KEYS = ["optimized_ensemble", "statistical", "lightgbm", "xgboost", "logistic_regression"]


def get_next_issue_no(issue_no: str) -> str:
    next_value = int(issue_no) + 1
    return str(next_value).zfill(len(issue_no))


def get_next_draw_datetime(draw_date) -> str:
    date = draw_date
    draw_weekdays = {1, 3, 6}
    while True:
        date = date + timedelta(days=1)
        if date.weekday() in draw_weekdays:
            return f"{date.isoformat()} 21:15"


def calculate_prize_level(red_hit_count: int, blue_hit: bool) -> str | None:
    if red_hit_count == 6 and blue_hit:
        return "一等奖"
    if red_hit_count == 6:
        return "二等奖"
    if red_hit_count == 5 and blue_hit:
        return "三等奖"
    if red_hit_count == 5 or (red_hit_count == 4 and blue_hit):
        return "四等奖"
    if red_hit_count == 4 or (red_hit_count == 3 and blue_hit):
        return "五等奖"
    if blue_hit:
        return "六等奖"
    return None


def normalize_probabilities(value: dict) -> dict[int, float]:
    return {int(key): probability for key, probability in value.items()}


class PredictionService:
    def __init__(self, db: Session):
        self.draw_repository = DrawRepository(db)
        self.model_repository = ModelRepository(db)
        self.prediction_repository = PredictionRepository(db)

    def run_prediction(self, request: PredictionRunRequest, run_type: str = "manual") -> list[ModelPredictionRead]:
        model_keys = request.model_keys or ["optimized_ensemble"]
        train_draws = self.draw_repository.list_until_issue(request.train_until_issue_no, inclusive=True)
        if not train_draws:
            raise ValueError("No training draws found for train_until_issue_no")

        run = self.prediction_repository.create_run(
            target_issue_no=request.target_issue_no,
            train_until_issue_no=request.train_until_issue_no,
            run_type=run_type,
            metadata={
                "model_keys": model_keys,
                "candidate_strategy": request.candidate_strategy,
                "candidate_count": request.candidate_count,
            },
        )
        predictions: list[ModelPredictionRead] = []
        for key in model_keys:
            db_model = self.model_repository.get_or_create_by_key(key)
            model = create_model(key)
            model.fit(train_draws)
            red_probabilities = model.predict_red_probabilities(features=None)
            blue_probabilities = model.predict_blue_probabilities(features=None)
            candidates = CandidateGenerator(strategy=request.candidate_strategy).generate(
                red_probabilities=red_probabilities,
                blue_probabilities=blue_probabilities,
                count=request.candidate_count,
            )
            self.prediction_repository.create_prediction(
                prediction_run_id=run.id,
                model_id=db_model.id,
                target_issue_no=request.target_issue_no,
                red_probabilities={str(k): v for k, v in red_probabilities.items()},
                blue_probabilities={str(k): v for k, v in blue_probabilities.items()},
                candidate_numbers=[candidate.model_dump() for candidate in candidates],
            )
            predictions.append(
                ModelPredictionRead(
                    model_key=key,
                    target_issue_no=request.target_issue_no,
                    train_until_issue_no=request.train_until_issue_no,
                    draw_datetime=get_next_draw_datetime(train_draws[-1].draw_date),
                    red_probabilities=red_probabilities,
                    blue_probabilities=blue_probabilities,
                    candidate_numbers=candidates,
                    prediction_run_id=run.id,
                    run_type=run_type,
                )
            )
        self.prediction_repository.commit()
        return predictions

    def list_latest_predictions(self) -> list[ModelPredictionRead]:
        predictions = []
        for prediction, run, model in self.prediction_repository.list_latest_predictions():
            predictions.append(
                ModelPredictionRead(
                    model_key=model.model_key,
                    target_issue_no=prediction.target_issue_no,
                    train_until_issue_no=run.train_until_issue_no,
                    draw_datetime=self._get_draw_datetime_for_train_issue(run.train_until_issue_no),
                    red_probabilities=normalize_probabilities(prediction.red_probabilities),
                    blue_probabilities=normalize_probabilities(prediction.blue_probabilities),
                    candidate_numbers=prediction.candidate_numbers,
                    prediction_run_id=run.id,
                    run_type=run.run_type,
                    best_red_hit_count=prediction.best_red_hit_count,
                    best_blue_hit=prediction.best_blue_hit,
                    evaluated_at=prediction.evaluated_at.isoformat() if prediction.evaluated_at else None,
                )
            )
        return predictions

    def _get_draw_datetime_for_train_issue(self, train_until_issue_no: str) -> str | None:
        train_draw = self.draw_repository.get_by_issue(train_until_issue_no)
        if train_draw is None:
            return None
        return get_next_draw_datetime(train_draw.draw_date)

    def evaluate_predictions_for_draw(self, draw: LotteryDraw) -> int:
        evaluated_count = 0
        actual_red_numbers = set(draw.red_numbers)
        for prediction in self.prediction_repository.list_predictions_for_issue(draw.issue_no):
            evaluated_candidates = []
            best_red_hit_count = 0
            best_blue_hit = False
            for candidate in prediction.candidate_numbers:
                red_hit_count = len(actual_red_numbers.intersection(candidate["red_numbers"]))
                blue_hit = candidate["blue_number"] == draw.blue_number
                best_red_hit_count = max(best_red_hit_count, red_hit_count)
                best_blue_hit = best_blue_hit or blue_hit
                evaluated_candidates.append(
                    {
                        **candidate,
                        "red_hit_count": red_hit_count,
                        "blue_hit": blue_hit,
                        "prize_level": calculate_prize_level(red_hit_count, blue_hit),
                    }
                )
            prediction.candidate_numbers = evaluated_candidates
            prediction.best_red_hit_count = best_red_hit_count
            prediction.best_blue_hit = best_blue_hit
            prediction.evaluated_at = datetime.now(timezone.utc)
            evaluated_count += 1
        if evaluated_count:
            self.prediction_repository.commit()
        return evaluated_count

    def run_auto_prediction_after_latest_draw(self) -> list[ModelPredictionRead]:
        latest_draw = self.draw_repository.get_latest()
        if latest_draw is None:
            return []
        target_issue_no = get_next_issue_no(latest_draw.issue_no)
        if self.prediction_repository.has_run_for_target(target_issue_no, run_type="auto"):
            return []
        return self.run_prediction(
            PredictionRunRequest(
                target_issue_no=target_issue_no,
                train_until_issue_no=latest_draw.issue_no,
                model_keys=DEFAULT_AUTO_MODEL_KEYS,
                candidate_strategy="optimized",
                candidate_count=5,
            ),
            run_type="auto",
        )
