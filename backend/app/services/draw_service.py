from sqlalchemy.orm import Session

from app.ml.features.draw_features import calculate_draw_features
from app.repositories.draw_repository import DrawRepository
from app.schemas.draw import LotteryDrawCreate, LotteryDrawImportResult


class DrawService:
    def __init__(self, db: Session):
        self.repository = DrawRepository(db)

    def list_draws(self, limit: int = 50, offset: int = 0):
        return self.repository.list_draws(limit=limit, offset=offset)

    def get_latest(self):
        return self.repository.get_latest()

    def get_by_issue(self, issue_no: str):
        return self.repository.get_by_issue(issue_no)

    def import_draws(
        self,
        draws: list[LotteryDrawCreate],
        overwrite: bool = True,
    ) -> LotteryDrawImportResult:
        created_count = 0
        updated_count = 0
        skipped_count = 0
        imported_issue_nos: list[str] = []

        for payload in sorted(draws, key=lambda item: (item.draw_date, item.issue_no)):
            existing = self.repository.get_by_issue(payload.issue_no)
            if existing is None:
                self.repository.create(payload)
                created_count += 1
                imported_issue_nos.append(payload.issue_no)
            elif overwrite:
                self.repository.update(existing, payload)
                updated_count += 1
                imported_issue_nos.append(payload.issue_no)
            else:
                skipped_count += 1

        self.repository.flush()
        self._recalculate_draw_features()
        self.repository.commit()
        self._evaluate_imported_draws_and_predict_next(imported_issue_nos)
        latest = self.repository.get_latest()

        return LotteryDrawImportResult(
            imported_count=len(draws),
            created_count=created_count,
            updated_count=updated_count,
            skipped_count=skipped_count,
            latest_issue_no=latest.issue_no if latest else None,
        )

    def _evaluate_imported_draws_and_predict_next(self, issue_nos: list[str]) -> None:
        if not issue_nos:
            return
        from app.services.prediction_service import PredictionService

        prediction_service = PredictionService(self.repository.db)
        for issue_no in issue_nos:
            draw = self.repository.get_by_issue(issue_no)
            if draw is not None:
                prediction_service.evaluate_predictions_for_draw(draw)
        prediction_service.run_auto_prediction_after_latest_draw()

    def _recalculate_draw_features(self) -> None:
        previous_red_numbers: list[int] | None = None
        for draw in self.repository.list_all_chronological():
            features = calculate_draw_features(
                red_numbers=draw.red_numbers,
                previous_red_numbers=previous_red_numbers,
            )
            for key, value in features.items():
                setattr(draw, key, value)
            previous_red_numbers = draw.red_numbers
