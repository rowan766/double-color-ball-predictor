from datetime import date
from types import SimpleNamespace

from app.schemas.draw import LotteryDrawCreate
from app.services.draw_service import DrawService


class FakeDrawRepository:
    def __init__(self):
        self.draws = {}
        self.committed = False
        self.flushed = False

    def get_by_issue(self, issue_no):
        return self.draws.get(issue_no)

    def get_latest(self):
        if not self.draws:
            return None
        return max(self.draws.values(), key=lambda draw: (draw.draw_date, draw.issue_no))

    def create(self, payload):
        draw = SimpleNamespace(id=len(self.draws) + 1, **payload.model_dump())
        self.draws[draw.issue_no] = draw
        return draw

    def update(self, draw, payload):
        for key, value in payload.model_dump().items():
            setattr(draw, key, value)
        return draw

    def list_all_chronological(self):
        return sorted(self.draws.values(), key=lambda draw: (draw.draw_date, draw.issue_no))

    def flush(self):
        self.flushed = True

    def commit(self):
        self.committed = True


def make_service():
    service = DrawService.__new__(DrawService)
    service.repository = FakeDrawRepository()
    return service


def test_import_draws_creates_and_recalculates_features():
    service = make_service()
    result = service.import_draws(
        [
            LotteryDrawCreate(
                issue_no="2024002",
                draw_date=date(2024, 1, 4),
                red_numbers=[1, 2, 3, 4, 5, 6],
                blue_number=7,
            ),
            LotteryDrawCreate(
                issue_no="2024001",
                draw_date=date(2024, 1, 2),
                red_numbers=[1, 8, 9, 10, 11, 12],
                blue_number=3,
            ),
        ]
    )

    assert result.created_count == 2
    assert result.updated_count == 0
    assert result.latest_issue_no == "2024002"
    assert service.repository.draws["2024002"].repeat_with_prev_count == 1
    assert service.repository.committed is True


def test_import_draws_skips_existing_when_overwrite_is_false():
    service = make_service()
    payload = LotteryDrawCreate(
        issue_no="2024001",
        draw_date=date(2024, 1, 2),
        red_numbers=[1, 2, 3, 4, 5, 6],
        blue_number=7,
    )
    service.import_draws([payload])
    result = service.import_draws(
        [
            LotteryDrawCreate(
                issue_no="2024001",
                draw_date=date(2024, 1, 2),
                red_numbers=[8, 9, 10, 11, 12, 13],
                blue_number=1,
            )
        ],
        overwrite=False,
    )

    assert result.skipped_count == 1
    assert service.repository.draws["2024001"].red_numbers == [1, 2, 3, 4, 5, 6]
