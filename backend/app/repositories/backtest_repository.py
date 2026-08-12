from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.backtest import BacktestResult, BacktestRun
from app.db.models.metric import ModelMetric
from app.db.models.model import MLModel


class BacktestRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_run(
        self,
        name: str,
        model_id: int,
        start_issue_no: str,
        end_issue_no: str,
        initial_train_size: int,
        candidate_strategy: str,
        config: dict,
    ) -> BacktestRun:
        run = BacktestRun(
            name=name,
            model_id=model_id,
            start_issue_no=start_issue_no,
            end_issue_no=end_issue_no,
            initial_train_size=initial_train_size,
            candidate_strategy=candidate_strategy,
            status="completed",
            config=config,
        )
        self.db.add(run)
        self.db.flush()
        return run

    def create_result(self, **kwargs) -> BacktestResult:
        result = BacktestResult(**kwargs)
        self.db.add(result)
        return result

    def create_metric(self, **kwargs) -> ModelMetric:
        metric = ModelMetric(**kwargs)
        self.db.add(metric)
        self.db.flush()
        return metric

    def commit(self) -> None:
        self.db.commit()

    def leaderboard(self, limit: int = 20) -> list[tuple[ModelMetric, MLModel]]:
        stmt = (
            select(ModelMetric, MLModel)
            .join(MLModel, MLModel.id == ModelMetric.model_id)
            .order_by(ModelMetric.ranking_score.desc(), ModelMetric.created_at.desc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).all())
