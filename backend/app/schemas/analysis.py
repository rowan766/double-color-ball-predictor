from pydantic import BaseModel


class FrequencyItem(BaseModel):
    number: int
    count: int
    frequency: float


class AnalysisSummary(BaseModel):
    total_draws: int
    red_frequency: list[FrequencyItem]
    blue_frequency: list[FrequencyItem]


class OmissionItem(BaseModel):
    number: int
    current_omission: int


class HotColdSummary(BaseModel):
    hot_reds: list[int]
    cold_reds: list[int]
    hot_blues: list[int]
    cold_blues: list[int]


class TrendPoint(BaseModel):
    issue_no: str
    red_sum: int | None
    red_span: int | None
    odd_count: int | None
    big_count: int | None
