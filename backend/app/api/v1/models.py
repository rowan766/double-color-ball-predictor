from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.model_service import ModelService

router = APIRouter()


@router.get("")
def list_models(db: Session = Depends(get_db)):
    return ModelService(db).list_supported_models()
