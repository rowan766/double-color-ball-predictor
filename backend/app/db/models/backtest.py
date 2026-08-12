from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class BacktestRun(Base):
    __tablename__ = "backtest_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    model_id: Mapped[int] = mapped_column(ForeignKey("ml_models.id"), nullable=False)
    start_issue_no: Mapped[str] = mapped_column(String(32), nullable=False)
    end_issue_no: Mapped[str] = mapped_column(String(32), nullable=False)
    initial_train_size: Mapped[int] = mapped_column(Integer, nullable=False)
    candidate_strategy: Mapped[str] = mapped_column(String(32), nullable=False, default="top_k")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BacktestResult(Base):
    __tablename__ = "backtest_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    backtest_run_id: Mapped[int] = mapped_column(ForeignKey("backtest_runs.id"), nullable=False)
    model_id: Mapped[int] = mapped_column(ForeignKey("ml_models.id"), nullable=False)
    target_issue_no: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    train_until_issue_no: Mapped[str] = mapped_column(String(32), nullable=False)
    predicted_red_numbers: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    predicted_blue_number: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_red_numbers: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    actual_blue_number: Mapped[int] = mapped_column(Integer, nullable=False)
    red_hit_count: Mapped[int] = mapped_column(Integer, nullable=False)
    blue_hit: Mapped[bool] = mapped_column(nullable=False)
    prize_level: Mapped[str | None] = mapped_column(String(32))
    red_probabilities: Mapped[dict] = mapped_column(JSONB, nullable=False)
    blue_probabilities: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
