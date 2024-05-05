from dataclasses import dataclass
from enum import Enum


class ModelTypeEnum(str, Enum):
    LOGISTIC_REGRESSION = 'logistic_regression'
    RANDOM_FOREST = 'random_forest'
    NEURAL_NETWORK = 'neural_network'


@dataclass
class Model:
    id: int
    dataset_id: int
    type: ModelTypeEnum
    progress: int
