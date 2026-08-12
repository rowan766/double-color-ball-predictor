from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class LotteryDraw(Base):
    __tablename__ = "lottery_draws"
    __table_args__ = (UniqueConstraint("issue_no", name="uq_lottery_draws_issue_no"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    issue_no: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    draw_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    red_numbers: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    blue_number: Mapped[int] = mapped_column(Integer, nullable=False)
    red_sum: Mapped[int | None] = mapped_column(Integer)
    red_span: Mapped[int | None] = mapped_column(Integer)
    odd_count: Mapped[int | None] = mapped_column(Integer)
    even_count: Mapped[int | None] = mapped_column(Integer)
    big_count: Mapped[int | None] = mapped_column(Integer)
    small_count: Mapped[int | None] = mapped_column(Integer)
    zone_1_count: Mapped[int | None] = mapped_column(Integer)
    zone_2_count: Mapped[int | None] = mapped_column(Integer)
    zone_3_count: Mapped[int | None] = mapped_column(Integer)
    consecutive_count: Mapped[int | None] = mapped_column(Integer)
    repeat_with_prev_count: Mapped[int | None] = mapped_column(Integer)
    prime_count: Mapped[int | None] = mapped_column(Integer)
    source: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
