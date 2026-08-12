from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analysis import AnalysisSummary
from app.services.analysis_service import AnalysisService

router = APIRouter()


@router.get("/summary", response_model=AnalysisSummary)
def get_summary(db: Session = Depends(get_db)):
    return AnalysisService(db).get_summary()


@router.get("/red-frequency")
def get_red_frequency(db: Session = Depends(get_db)):
    return AnalysisService(db).get_summary().red_frequency


@router.get("/blue-frequency")
def get_blue_frequency(db: Session = Depends(get_db)):
    return AnalysisService(db).get_summary().blue_frequency


@router.get("/hot-cold")
def get_hot_cold(db: Session = Depends(get_db)):
    return AnalysisService(db).get_hot_cold()


@router.get("/omission")
def get_omission(db: Session = Depends(get_db)):
    return AnalysisService(db).get_red_omission()


@router.get("/trends")
def get_trends(db: Session = Depends(get_db)):
    return AnalysisService(db).get_trends()
