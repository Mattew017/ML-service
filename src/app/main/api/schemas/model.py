from pydantic import BaseModel, Field

from app.application.models.metric import Metric
from app.application.models.model import Model


class GetModelResponseSchema(BaseModel):
    model: Model
    metrics: list[Metric] | None
