from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.draw import LotteryDrawImportRequest, LotteryDrawImportResult, LotteryDrawRead
from app.services.draw_service import DrawService

router = APIRouter()


@router.get("", response_model=list[LotteryDrawRead])
def list_draws(
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return DrawService(db).list_draws(limit=limit, offset=offset)


@router.post("/import", response_model=LotteryDrawImportResult)
def import_draws(request: LotteryDrawImportRequest, db: Session = Depends(get_db)):
    return DrawService(db).import_draws(draws=request.draws, overwrite=request.overwrite)


@router.get("/latest", response_model=LotteryDrawRead)
def get_latest_draw(db: Session = Depends(get_db)):
    draw = DrawService(db).get_latest()
    if draw is None:
        raise HTTPException(status_code=404, detail="No draw data found")
    return draw


@router.get("/{issue_no}", response_model=LotteryDrawRead)
def get_draw(issue_no: str, db: Session = Depends(get_db)):
    draw = DrawService(db).get_by_issue(issue_no)
    if draw is None:
        raise HTTPException(status_code=404, detail="Draw not found")
    return draw
