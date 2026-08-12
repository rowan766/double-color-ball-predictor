from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.draw import LotteryDraw
from app.schemas.draw import LotteryDrawCreate


class DrawRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_draws(self, limit: int = 50, offset: int = 0) -> list[LotteryDraw]:
        stmt = select(LotteryDraw).order_by(LotteryDraw.draw_date.desc()).offset(offset).limit(limit)
        return list(self.db.scalars(stmt))

    def list_all_chronological(self) -> list[LotteryDraw]:
        stmt = select(LotteryDraw).order_by(LotteryDraw.draw_date.asc(), LotteryDraw.issue_no.asc())
        return list(self.db.scalars(stmt))

    def list_until_issue(self, issue_no: str, inclusive: bool = True) -> list[LotteryDraw]:
        operator = LotteryDraw.issue_no <= issue_no if inclusive else LotteryDraw.issue_no < issue_no
        stmt = (
            select(LotteryDraw)
            .where(operator)
            .order_by(LotteryDraw.draw_date.asc(), LotteryDraw.issue_no.asc())
        )
        return list(self.db.scalars(stmt))

    def list_issue_range(self, start_issue_no: str, end_issue_no: str) -> list[LotteryDraw]:
        stmt = (
            select(LotteryDraw)
            .where(LotteryDraw.issue_no >= start_issue_no, LotteryDraw.issue_no <= end_issue_no)
            .order_by(LotteryDraw.draw_date.asc(), LotteryDraw.issue_no.asc())
        )
        return list(self.db.scalars(stmt))

    def get_latest(self) -> LotteryDraw | None:
        stmt = select(LotteryDraw).order_by(LotteryDraw.draw_date.desc()).limit(1)
        return self.db.scalar(stmt)

    def get_by_issue(self, issue_no: str) -> LotteryDraw | None:
        stmt = select(LotteryDraw).where(LotteryDraw.issue_no == issue_no)
        return self.db.scalar(stmt)

    def count(self) -> int:
        return self.db.scalar(select(func.count()).select_from(LotteryDraw)) or 0

    def create(self, payload: LotteryDrawCreate) -> LotteryDraw:
        draw = LotteryDraw(**payload.model_dump())
        self.db.add(draw)
        return draw

    def update(self, draw: LotteryDraw, payload: LotteryDrawCreate) -> LotteryDraw:
        for key, value in payload.model_dump().items():
            setattr(draw, key, value)
        return draw

    def commit(self) -> None:
        self.db.commit()

    def flush(self) -> None:
        self.db.flush()
