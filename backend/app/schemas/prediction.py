from pydantic import BaseModel


class CandidateNumbers(BaseModel):
    red_numbers: list[int]
    blue_number: int
    score: float | None = None
    red_hit_count: int | None = None
    blue_hit: bool | None = None
    prize_level: str | None = None


class PredictionRunRequest(BaseModel):
    target_issue_no: str
    train_until_issue_no: str
    model_keys: list[str] | None = None
    candidate_strategy: str = "top_k"
    candidate_count: int = 5


class ModelPredictionRead(BaseModel):
    model_key: str
    target_issue_no: str
    train_until_issue_no: str
    draw_datetime: str | None = None
    red_probabilities: dict[int, float]
    blue_probabilities: dict[int, float]
    candidate_numbers: list[CandidateNumbers]
    prediction_run_id: int | None = None
    run_type: str | None = None
    best_red_hit_count: int | None = None
    best_blue_hit: bool | None = None
    evaluated_at: str | None = None
