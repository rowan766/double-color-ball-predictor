from fastapi import APIRouter

from app.api.v1 import analysis, backtests, dashboard, draws, models, predictions

api_router = APIRouter()


@api_router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


api_router.include_router(draws.router, prefix="/draws", tags=["draws"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(backtests.router, prefix="/backtests", tags=["backtests"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
