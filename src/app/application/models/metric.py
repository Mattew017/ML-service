from dataclasses import dataclass
from enum import Enum


class MetricsEnum(str, Enum):
    ACCURACY = 'accuracy'
    PRECISION = 'precision'
    RECALL = 'recall'
    F1 = 'f1'


@dataclass
class Metric:
    name: str
    value: float
