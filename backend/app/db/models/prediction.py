from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class PredictionRun(Base):
    __tablename__ = "prediction_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    target_issue_no: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    train_until_issue_no: Mapped[str] = mapped_column(String(32), nullable=False)
    run_type: Mapped[str] = mapped_column(String(32), nullable=False, default="manual")
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ModelPrediction(Base):
    __tablename__ = "model_predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    prediction_run_id: Mapped[int] = mapped_column(ForeignKey("prediction_runs.id"), nullable=False)
    model_id: Mapped[int] = mapped_column(ForeignKey("ml_models.id"), nullable=False)
    target_issue_no: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    red_probabilities: Mapped[dict] = mapped_column(JSONB, nullable=False)
    blue_probabilities: Mapped[dict] = mapped_column(JSONB, nullable=False)
    candidate_numbers: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    best_red_hit_count: Mapped[int | None] = mapped_column(Integer)
    best_blue_hit: Mapped[bool | None] = mapped_column(Boolean)
    evaluated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    model_artifact_path: Mapped[str | None] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
