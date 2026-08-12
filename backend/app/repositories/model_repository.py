from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.model import MLModel
from app.ml.models.registry import MODEL_REGISTRY


class ModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_active(self) -> list[MLModel]:
        stmt = select(MLModel).where(MLModel.is_active.is_(True)).order_by(MLModel.id)
        return list(self.db.scalars(stmt))

    def get_by_key(self, model_key: str) -> MLModel | None:
        stmt = select(MLModel).where(MLModel.model_key == model_key, MLModel.is_active.is_(True)).limit(1)
        return self.db.scalar(stmt)

    def get_or_create_by_key(self, model_key: str) -> MLModel:
        existing = self.get_by_key(model_key)
        if existing is not None:
            return existing
        model_cls = MODEL_REGISTRY[model_key]
        model = MLModel(
            model_key=model_key,
            model_name=model_cls.display_name,
            model_type=model_cls.model_type,
            version="v1",
            params={},
            is_active=True,
        )
        self.db.add(model)
        self.db.flush()
        return model
