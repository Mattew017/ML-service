from pydantic import BaseModel, Field

from app.application.models.dataset import DatasetData, DatasetType


class CreateDatasetRequest(BaseModel):
    name: str
    type: DatasetType
    data: list[DatasetData]


class CreateDatasetResponse(BaseModel):
    id: int
