from app.ml.models.sklearn_binary_model import OptionalBinaryClassifierModel


class LightGBMLotteryModel(OptionalBinaryClassifierModel):
    model_key = "lightgbm"
    display_name = "LightGBM"
    model_type = "gradient_boosting"
    classifier_kind = "lightgbm"
