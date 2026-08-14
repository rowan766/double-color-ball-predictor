from app.ml.models.base import BaseLotteryModel
from app.ml.models.lightgbm_model import LightGBMLotteryModel
from app.ml.models.logistic_regression_model import LogisticRegressionLotteryModel
from app.ml.models.optimized_ensemble_model import OptimizedEnsembleModel
from app.ml.models.random_baseline import RandomBaselineModel
from app.ml.models.statistical_model import StatisticalModel
from app.ml.models.xgboost_model import XGBoostLotteryModel

MODEL_REGISTRY: dict[str, type[BaseLotteryModel]] = {
    RandomBaselineModel.model_key: RandomBaselineModel,
    StatisticalModel.model_key: StatisticalModel,
    LogisticRegressionLotteryModel.model_key: LogisticRegressionLotteryModel,
    LightGBMLotteryModel.model_key: LightGBMLotteryModel,
    XGBoostLotteryModel.model_key: XGBoostLotteryModel,
    OptimizedEnsembleModel.model_key: OptimizedEnsembleModel,
}


def create_model(model_key: str) -> BaseLotteryModel:
    try:
        return MODEL_REGISTRY[model_key]()
    except KeyError as exc:
        raise ValueError(f"Unsupported model_key: {model_key}") from exc
