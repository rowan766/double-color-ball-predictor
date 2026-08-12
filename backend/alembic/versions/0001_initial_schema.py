"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-08-13
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "lottery_draws",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("issue_no", sa.String(length=32), nullable=False),
        sa.Column("draw_date", sa.Date(), nullable=False),
        sa.Column("red_numbers", postgresql.ARRAY(sa.Integer()), nullable=False),
        sa.Column("blue_number", sa.Integer(), nullable=False),
        sa.Column("red_sum", sa.Integer(), nullable=True),
        sa.Column("red_span", sa.Integer(), nullable=True),
        sa.Column("odd_count", sa.Integer(), nullable=True),
        sa.Column("even_count", sa.Integer(), nullable=True),
        sa.Column("big_count", sa.Integer(), nullable=True),
        sa.Column("small_count", sa.Integer(), nullable=True),
        sa.Column("zone_1_count", sa.Integer(), nullable=True),
        sa.Column("zone_2_count", sa.Integer(), nullable=True),
        sa.Column("zone_3_count", sa.Integer(), nullable=True),
        sa.Column("consecutive_count", sa.Integer(), nullable=True),
        sa.Column("repeat_with_prev_count", sa.Integer(), nullable=True),
        sa.Column("prime_count", sa.Integer(), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("issue_no", name="uq_lottery_draws_issue_no"),
    )
    op.create_index("ix_lottery_draws_draw_date", "lottery_draws", ["draw_date"])
    op.create_index("ix_lottery_draws_issue_no", "lottery_draws", ["issue_no"])

    op.create_table(
        "ml_models",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("model_key", sa.String(length=64), nullable=False),
        sa.Column("model_name", sa.String(length=128), nullable=False),
        sa.Column("model_type", sa.String(length=64), nullable=False),
        sa.Column("version", sa.String(length=32), nullable=False),
        sa.Column("params", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ml_models_model_key", "ml_models", ["model_key"])

    op.create_table(
        "prediction_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("target_issue_no", sa.String(length=32), nullable=False),
        sa.Column("train_until_issue_no", sa.String(length=32), nullable=False),
        sa.Column("run_type", sa.String(length=32), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_prediction_runs_target_issue_no", "prediction_runs", ["target_issue_no"])

    op.create_table(
        "backtest_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("model_id", sa.Integer(), nullable=False),
        sa.Column("start_issue_no", sa.String(length=32), nullable=False),
        sa.Column("end_issue_no", sa.String(length=32), nullable=False),
        sa.Column("initial_train_size", sa.Integer(), nullable=False),
        sa.Column("candidate_strategy", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("config", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["model_id"], ["ml_models.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "model_predictions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("prediction_run_id", sa.Integer(), nullable=False),
        sa.Column("model_id", sa.Integer(), nullable=False),
        sa.Column("target_issue_no", sa.String(length=32), nullable=False),
        sa.Column("red_probabilities", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("blue_probabilities", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("candidate_numbers", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("model_artifact_path", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["model_id"], ["ml_models.id"]),
        sa.ForeignKeyConstraint(["prediction_run_id"], ["prediction_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_model_predictions_target_issue_no", "model_predictions", ["target_issue_no"])

    op.create_table(
        "backtest_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("backtest_run_id", sa.Integer(), nullable=False),
        sa.Column("model_id", sa.Integer(), nullable=False),
        sa.Column("target_issue_no", sa.String(length=32), nullable=False),
        sa.Column("train_until_issue_no", sa.String(length=32), nullable=False),
        sa.Column("predicted_red_numbers", postgresql.ARRAY(sa.Integer()), nullable=False),
        sa.Column("predicted_blue_number", sa.Integer(), nullable=False),
        sa.Column("actual_red_numbers", postgresql.ARRAY(sa.Integer()), nullable=False),
        sa.Column("actual_blue_number", sa.Integer(), nullable=False),
        sa.Column("red_hit_count", sa.Integer(), nullable=False),
        sa.Column("blue_hit", sa.Boolean(), nullable=False),
        sa.Column("prize_level", sa.String(length=32), nullable=True),
        sa.Column("red_probabilities", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("blue_probabilities", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["backtest_run_id"], ["backtest_runs.id"]),
        sa.ForeignKeyConstraint(["model_id"], ["ml_models.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_backtest_results_target_issue_no", "backtest_results", ["target_issue_no"])

    op.create_table(
        "model_metrics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("model_id", sa.Integer(), nullable=False),
        sa.Column("backtest_run_id", sa.Integer(), nullable=False),
        sa.Column("total_predictions", sa.Integer(), nullable=False),
        sa.Column("avg_red_hits", sa.Float(), nullable=False),
        sa.Column("blue_hit_rate", sa.Float(), nullable=False),
        sa.Column("red_hit_distribution", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("prize_distribution", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("random_baseline_diff", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("ranking_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["backtest_run_id"], ["backtest_runs.id"]),
        sa.ForeignKeyConstraint(["model_id"], ["ml_models.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("model_metrics")
    op.drop_index("ix_backtest_results_target_issue_no", table_name="backtest_results")
    op.drop_table("backtest_results")
    op.drop_index("ix_model_predictions_target_issue_no", table_name="model_predictions")
    op.drop_table("model_predictions")
    op.drop_table("backtest_runs")
    op.drop_index("ix_prediction_runs_target_issue_no", table_name="prediction_runs")
    op.drop_table("prediction_runs")
    op.drop_index("ix_ml_models_model_key", table_name="ml_models")
    op.drop_table("ml_models")
    op.drop_index("ix_lottery_draws_issue_no", table_name="lottery_draws")
    op.drop_index("ix_lottery_draws_draw_date", table_name="lottery_draws")
    op.drop_table("lottery_draws")
