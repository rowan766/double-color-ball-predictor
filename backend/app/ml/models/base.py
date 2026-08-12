from abc import ABC, abstractmethod


class BaseLotteryModel(ABC):
    model_key: str
    display_name: str
    model_type: str

    def fit(self, train_draws: list) -> None:
        self.train_draws = train_draws

    @abstractmethod
    def predict_red_probabilities(self, features) -> dict[int, float]:
        raise NotImplementedError

    @abstractmethod
    def predict_blue_probabilities(self, features) -> dict[int, float]:
        raise NotImplementedError
