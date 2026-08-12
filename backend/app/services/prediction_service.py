from app.ml.models.registry import create_model
from app.ml.prediction.candidate_generator import CandidateGenerator
from app.repositories.draw_repository import DrawRepository
from app.repositories.model_repository import ModelRepository
from app.repositories.prediction_repository import PredictionRepository
from app.schemas.prediction import ModelPredictionRead, PredictionRunRequest
from sqlalchemy.orm import Session


class PredictionService:
    def __init__(self, db: Session):
        self.draw_repository = DrawRepository(db)
        self.model_repository = ModelRepository(db)
        self.prediction_repository = PredictionRepository(db)

    def run_prediction(self, request: PredictionRunRequest) -> list[ModelPredictionRead]:
        model_keys = request.model_keys or ["random_baseline"]
        train_draws = self.draw_repository.list_until_issue(request.train_until_issue_no, inclusive=True)
        if not train_draws:
            raise ValueError("No training draws found for train_until_issue_no")

        run = self.prediction_repository.create_run(
            target_issue_no=request.target_issue_no,
            train_until_issue_no=request.train_until_issue_no,
            run_type="manual",
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
                    red_probabilities=red_probabilities,
                    blue_probabilities=blue_probabilities,
                    candidate_numbers=candidates,
                    prediction_run_id=run.id,
                )
            )
        self.prediction_repository.commit()
        return predictions
