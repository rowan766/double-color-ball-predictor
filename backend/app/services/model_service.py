from sqlalchemy.orm import Session

from app.ml.models.registry import MODEL_REGISTRY


class ModelService:
    def __init__(self, db: Session):
        self.db = db

    def list_supported_models(self) -> list[dict]:
        return [
            {"model_key": key, "model_name": cls.display_name, "model_type": cls.model_type}
            for key, cls in MODEL_REGISTRY.items()
        ]
