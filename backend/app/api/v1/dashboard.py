from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.draw import LotteryDrawRead
from app.services.analysis_service import AnalysisService
from app.services.draw_service import DrawService

router = APIRouter()


@router.get("")
def get_dashboard(db: Session = Depends(get_db)):
    latest_draw = DrawService(db).get_latest()
    analysis_summary = AnalysisService(db).get_summary()
    return {
        "latest_draw": LotteryDrawRead.model_validate(latest_draw).model_dump(mode="json")
        if latest_draw
        else None,
        "total_draws": analysis_summary.total_draws,
        "latest_predictions": [],
        "model_leaderboard": [],
        "recent_backtest_metrics": [],
        "red_probability_chart": [],
        "blue_probability_chart": [],
    }
