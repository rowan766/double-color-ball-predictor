from sqlalchemy.orm import Session

from app.services.prediction_service import PredictionService


def evaluate_after_draw_task(db: Session, issue_no: str) -> int:
    """Evaluate predictions after a new draw result is available."""
    draw = PredictionService(db).draw_repository.get_by_issue(issue_no)
    if draw is None:
        return 0
    return PredictionService(db).evaluate_predictions_for_draw(draw)
