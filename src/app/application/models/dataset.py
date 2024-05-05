from dataclasses import dataclass, field
from enum import Enum


class DatasetType(str, Enum):
    TRAIN = "train"
    TEST = "test"

@dataclass
class DatasetData:
    id: int
    param1: float
    param2: float
    target: float


@dataclass
class Dataset:
    id: int = field(init=False)
    name: str
    type: str
    data: list[DatasetData]
