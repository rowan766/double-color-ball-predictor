from datetime import date

from pydantic import BaseModel, Field, field_validator


class LotteryDrawBase(BaseModel):
    issue_no: str
    draw_date: date
    red_numbers: list[int] = Field(min_length=6, max_length=6)
    blue_number: int = Field(ge=1, le=16)

    @field_validator("red_numbers")
    @classmethod
    def validate_red_numbers(cls, value: list[int]) -> list[int]:
        if len(set(value)) != 6:
            raise ValueError("red_numbers must contain 6 unique numbers")
        if any(number < 1 or number > 33 for number in value):
            raise ValueError("red_numbers must be between 1 and 33")
        return sorted(value)


class LotteryDrawCreate(LotteryDrawBase):
    source: str | None = None


class LotteryDrawImportRequest(BaseModel):
    draws: list[LotteryDrawCreate] = Field(min_length=1)
    overwrite: bool = True


class LotteryDrawImportResult(BaseModel):
    imported_count: int
    created_count: int
    updated_count: int
    skipped_count: int
    latest_issue_no: str | None = None


class LotteryDrawRead(LotteryDrawBase):
    id: int
    red_sum: int | None = None
    red_span: int | None = None
    odd_count: int | None = None
    even_count: int | None = None
    big_count: int | None = None
    small_count: int | None = None
    zone_1_count: int | None = None
    zone_2_count: int | None = None
    zone_3_count: int | None = None
    consecutive_count: int | None = None
    repeat_with_prev_count: int | None = None
    prime_count: int | None = None
    source: str | None = None

    model_config = {"from_attributes": True}
