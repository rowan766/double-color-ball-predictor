from abc import ABC, abstractmethod


class BaseFeatureBuilder(ABC):
    @abstractmethod
    def transform(self, draws, target_issue_no: str):
        raise NotImplementedError
