from pydantic import BaseModel, Field


class BacktestRunRequest(BaseModel):
    name: str
    model_keys: list[str]
    start_issue_no: str
    end_issue_no: str
    initial_train_size: int = 100
    candidate_strategy: str = "top_k"


class BacktestMetricRead(BaseModel):
    model_key: str
    backtest_run_id: int | None = None
    total_predictions: int
    avg_red_hits: float
    blue_hit_rate: float
    red_hit_distribution: dict[str, float]
    prize_distribution: dict[str, int]
    random_baseline_diff: dict[str, float] = Field(default_factory=dict)
    ranking_score: float
