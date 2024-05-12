from abc import ABC, abstractmethod

from app.application.models.dataset import Dataset
from app.application.models.metric import Metric
from app.application.models.model import Model
from app.application.models.user import User


class UoW(ABC):
    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UserDatabaseGateway(ABC):
    @abstractmethod
    async def add_user(self, user: User) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, id_: int) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_users(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        raise NotImplementedError


class DatasetDatabaseGateway(ABC):
    @abstractmethod
    async def add_dataset(self, dataset: Dataset) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_dataset_by_id(self, id_: int) -> Dataset | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_user_datasets(self, user_id: int) -> list[Dataset]:
        raise NotImplementedError

    @abstractmethod
    async def delete_dataset(self, dataset_id: int) -> None:
        raise NotImplementedError


class ModelDatabaseGateway(ABC):
    @abstractmethod
    async def add_train_model(self, model: Model) -> int:
        raise NotImplementedError

    @abstractmethod
    async def add_eval_model(self, model_id: int, dataset_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_train_model(self, model_id: int) -> Model | None:
        raise NotImplementedError

    @abstractmethod
    async def get_eval_model(self, model_id: int) -> Model | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_train_models(self, dataset_id: int) -> list[Model]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_eval_models(self, dataset_id: int) -> list[Model]:
        raise NotImplementedError

    @abstractmethod
    async def delete_train_model(self, model_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_eval_model(self, eval_model_id: int) -> None:
        raise NotImplementedError


class MetricDatabaseGateway(ABC):
    @abstractmethod
    async def add_train_metric(self, model_id: int, metric: Metric) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_eval_metric(self, eval_model_id: int, metric: Metric) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_train_metrics(self, model_id: int) -> list[Metric]:
        raise NotImplementedError

    @abstractmethod
    async def get_eval_metrics(self, eval_model_id: int) -> list[Metric]:
        raise NotImplementedError
