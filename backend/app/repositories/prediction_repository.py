from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.model import MLModel
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

    def has_run_for_target(self, target_issue_no: str, run_type: str | None = None) -> bool:
        stmt = select(PredictionRun.id).where(PredictionRun.target_issue_no == target_issue_no)
        if run_type is not None:
            stmt = stmt.where(PredictionRun.run_type == run_type)
        return self.db.scalar(stmt.limit(1)) is not None

    def list_predictions_for_issue(self, target_issue_no: str) -> list[ModelPrediction]:
        stmt = select(ModelPrediction).where(ModelPrediction.target_issue_no == target_issue_no)
        return list(self.db.scalars(stmt))

    def list_latest_predictions(self, limit: int = 50) -> list[tuple[ModelPrediction, PredictionRun, MLModel]]:
        latest_run = self.db.scalar(select(PredictionRun).order_by(PredictionRun.created_at.desc()).limit(1))
        if latest_run is None:
            return []
        stmt = (
            select(ModelPrediction, PredictionRun, MLModel)
            .join(PredictionRun, PredictionRun.id == ModelPrediction.prediction_run_id)
            .join(MLModel, MLModel.id == ModelPrediction.model_id)
            .where(PredictionRun.id == latest_run.id)
            .order_by(ModelPrediction.id.asc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).all())

    def commit(self) -> None:
        self.db.commit()
