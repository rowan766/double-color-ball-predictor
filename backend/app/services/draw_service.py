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

        for payload in sorted(draws, key=lambda item: (item.draw_date, item.issue_no)):
            existing = self.repository.get_by_issue(payload.issue_no)
            if existing is None:
                self.repository.create(payload)
                created_count += 1
            elif overwrite:
                self.repository.update(existing, payload)
                updated_count += 1
            else:
                skipped_count += 1

        self.repository.flush()
        self._recalculate_draw_features()
        self.repository.commit()
        latest = self.repository.get_latest()

        return LotteryDrawImportResult(
            imported_count=len(draws),
            created_count=created_count,
            updated_count=updated_count,
            skipped_count=skipped_count,
            latest_issue_no=latest.issue_no if latest else None,
        )

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
