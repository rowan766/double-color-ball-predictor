from collections import Counter

from sqlalchemy.orm import Session

from app.repositories.draw_repository import DrawRepository
from app.schemas.analysis import AnalysisSummary, FrequencyItem, HotColdSummary, OmissionItem, TrendPoint


class AnalysisService:
    def __init__(self, db: Session):
        self.draw_repository = DrawRepository(db)

    def get_summary(self) -> AnalysisSummary:
        draws = self.draw_repository.list_draws(limit=10_000)
        red_counter: Counter[int] = Counter()
        blue_counter: Counter[int] = Counter()
        for draw in draws:
            red_counter.update(draw.red_numbers)
            blue_counter.update([draw.blue_number])
        total = len(draws)
        red_total = total * 6 if total else 1
        blue_total = total if total else 1
        return AnalysisSummary(
            total_draws=total,
            red_frequency=[
                FrequencyItem(number=n, count=red_counter[n], frequency=red_counter[n] / red_total)
                for n in range(1, 34)
            ],
            blue_frequency=[
                FrequencyItem(number=n, count=blue_counter[n], frequency=blue_counter[n] / blue_total)
                for n in range(1, 17)
            ],
        )

    def get_hot_cold(self) -> HotColdSummary:
        summary = self.get_summary()
        red_sorted = sorted(summary.red_frequency, key=lambda item: (-item.count, item.number))
        blue_sorted = sorted(summary.blue_frequency, key=lambda item: (-item.count, item.number))
        return HotColdSummary(
            hot_reds=[item.number for item in red_sorted[:6]],
            cold_reds=[item.number for item in red_sorted[-6:]],
            hot_blues=[item.number for item in blue_sorted[:3]],
            cold_blues=[item.number for item in blue_sorted[-3:]],
        )

    def get_red_omission(self) -> list[OmissionItem]:
        draws = self.draw_repository.list_all_chronological()
        omissions = {number: 0 for number in range(1, 34)}
        for draw in draws:
            appeared = set(draw.red_numbers)
            for number in omissions:
                omissions[number] = 0 if number in appeared else omissions[number] + 1
        return [
            OmissionItem(number=number, current_omission=omission)
            for number, omission in sorted(omissions.items())
        ]

    def get_trends(self, limit: int = 50) -> list[TrendPoint]:
        draws = list(reversed(self.draw_repository.list_draws(limit=limit)))
        return [
            TrendPoint(
                issue_no=draw.issue_no,
                red_sum=draw.red_sum,
                red_span=draw.red_span,
                odd_count=draw.odd_count,
                big_count=draw.big_count,
            )
            for draw in draws
        ]
