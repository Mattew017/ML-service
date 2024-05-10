from dataclasses import dataclass, Field, asdict
from enum import Enum


class ModelTypeEnum(str, Enum):
    LOGISTIC_REGRESSION = 'logistic_regression'
    RANDOM_FOREST = 'random_forest'
    NEURAL_NETWORK = 'neural_network'


model_type_to_db = {
    ModelTypeEnum.LOGISTIC_REGRESSION: 1,
    ModelTypeEnum.RANDOM_FOREST: 2,
    ModelTypeEnum.NEURAL_NETWORK: 3
}


@dataclass
class Model:
    dataset_id: int
    type: ModelTypeEnum
    progress: int = 0
    id: int = 0

    def dict(self):
        return asdict(self)


