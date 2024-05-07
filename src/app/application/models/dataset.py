from dataclasses import dataclass, field
from enum import Enum


class DatasetType(str, Enum):
    TRAIN = "train"
    TEST = "test"


@dataclass
class DatasetData:
    param1: float
    param2: float
    target: float


@dataclass
class Dataset:
    user_id: int
    name: str
    type: DatasetType
    data: list[DatasetData]
    id: int = 0
