from app.ml.models.sklearn_binary_model import OptionalBinaryClassifierModel


class LogisticRegressionLotteryModel(OptionalBinaryClassifierModel):
    model_key = "logistic_regression"
    display_name = "Logistic Regression"
    model_type = "sklearn"
    classifier_kind = "sklearn_logistic"
