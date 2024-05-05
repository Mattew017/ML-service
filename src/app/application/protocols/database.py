from abc import ABC, abstractmethod

from app.application.models.dataset import Dataset
from app.application.models.metric import Metric
from app.application.models.model import Model
from app.application.models.user import User


class UoW(ABC):
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def flush(self):
        raise NotImplementedError


class UserDatabaseGateway(ABC):
    @abstractmethod
    def add_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_id(self, id_: int) -> User:
        raise NotImplementedError


class DatasetDatabaseGateway(ABC):
    @abstractmethod
    def add_dataset(self, dataset: Dataset) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_dataset_by_id(self, id_: int) -> Dataset:
        raise NotImplementedError

    @abstractmethod
    def get_all_user_datasets(self, user_id: int) -> list[Dataset]:
        raise NotImplementedError


class ModelDatabaseGateway(ABC):
    @abstractmethod
    def add_train_model(self, model: Model) -> int:
        raise NotImplementedError

    @abstractmethod
    def eval_model(self, model_id: int, dataset_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_train_model(self, model_id: int) -> Model:
        raise NotImplementedError

    @abstractmethod
    def get_eval_model(self, model_id: int) -> Model:
        raise NotImplementedError

    @abstractmethod
    def get_all_train_models(self, dataset_id: int) -> list[Model]:
        raise NotImplementedError

    @abstractmethod
    def get_all_eval_models(self, dataset_id: int) -> list[Model]:
        raise NotImplementedError


class MetricDatabaseGateway(ABC):
    @abstractmethod
    def get_train_metrics(self, model_id: int) -> list[Metric]:
        raise NotImplementedError

    @abstractmethod
    def get_eval_metrics(self, eval_model_id: int) -> list[Metric]:
        raise NotImplementedError
