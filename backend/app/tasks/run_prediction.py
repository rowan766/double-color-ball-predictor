from sqlalchemy.orm import Session

from app.schemas.prediction import ModelPredictionRead
from app.services.prediction_service import PredictionService


def run_prediction_task(db: Session) -> list[ModelPredictionRead]:
    """Run scheduled prediction after the prediction service is persisted."""
    return PredictionService(db).run_auto_prediction_after_latest_draw()
