from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.backtest import BacktestMetricRead, BacktestRunRequest
from app.services.backtest_service import BacktestService

router = APIRouter()


@router.post("/run", response_model=list[BacktestMetricRead])
def run_backtest(request: BacktestRunRequest, db: Session = Depends(get_db)):
    try:
        return BacktestService(db).run_backtest(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    return BacktestService(db).leaderboard()
