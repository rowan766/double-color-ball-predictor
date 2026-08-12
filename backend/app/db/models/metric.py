from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class ModelMetric(Base):
    __tablename__ = "model_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("ml_models.id"), nullable=False)
    backtest_run_id: Mapped[int] = mapped_column(ForeignKey("backtest_runs.id"), nullable=False)
    total_predictions: Mapped[int] = mapped_column(Integer, nullable=False)
    avg_red_hits: Mapped[float] = mapped_column(Float, nullable=False)
    blue_hit_rate: Mapped[float] = mapped_column(Float, nullable=False)
    red_hit_distribution: Mapped[dict] = mapped_column(JSONB, nullable=False)
    prize_distribution: Mapped[dict] = mapped_column(JSONB, nullable=False)
    random_baseline_diff: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    ranking_score: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
