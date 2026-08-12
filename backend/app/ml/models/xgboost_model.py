from app.ml.models.sklearn_binary_model import OptionalBinaryClassifierModel


class XGBoostLotteryModel(OptionalBinaryClassifierModel):
    model_key = "xgboost"
    display_name = "XGBoost"
    model_type = "gradient_boosting"
    classifier_kind = "xgboost"
