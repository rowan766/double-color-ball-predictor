from sqlalchemy.orm import Session

from app.db.models.prediction import ModelPrediction, PredictionRun


class PredictionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_run(
        self,
        target_issue_no: str,
        train_until_issue_no: str,
        run_type: str = "manual",
        metadata: dict | None = None,
    ) -> PredictionRun:
        run = PredictionRun(
            target_issue_no=target_issue_no,
            train_until_issue_no=train_until_issue_no,
            run_type=run_type,
            metadata_json=metadata or {},
        )
        self.db.add(run)
        self.db.flush()
        return run

    def create_prediction(
        self,
        prediction_run_id: int,
        model_id: int,
        target_issue_no: str,
        red_probabilities: dict,
        blue_probabilities: dict,
        candidate_numbers: list,
        model_artifact_path: str | None = None,
    ) -> ModelPrediction:
        prediction = ModelPrediction(
            prediction_run_id=prediction_run_id,
            model_id=model_id,
            target_issue_no=target_issue_no,
            red_probabilities=red_probabilities,
            blue_probabilities=blue_probabilities,
            candidate_numbers=candidate_numbers,
            model_artifact_path=model_artifact_path,
        )
        self.db.add(prediction)
        self.db.flush()
        return prediction

    def commit(self) -> None:
        self.db.commit()
