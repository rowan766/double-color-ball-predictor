from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.prediction import ModelPredictionRead, PredictionRunRequest
from app.services.prediction_service import PredictionService

router = APIRouter()


@router.post("/run", response_model=list[ModelPredictionRead])
def run_prediction(request: PredictionRunRequest, db: Session = Depends(get_db)):
    try:
        return PredictionService(db).run_prediction(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/latest")
def get_latest_prediction(db: Session = Depends(get_db)):
    return PredictionService(db).list_latest_predictions()


@router.post("/auto-next", response_model=list[ModelPredictionRead])
def run_auto_next_prediction(db: Session = Depends(get_db)):
    return PredictionService(db).run_auto_prediction_after_latest_draw()
