class ProbabilityPredictor:
    def predict(self, model, features):
        return {
            "red_probabilities": model.predict_red_probabilities(features),
            "blue_probabilities": model.predict_blue_probabilities(features),
        }
