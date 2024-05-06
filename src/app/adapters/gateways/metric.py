from sqlalchemy.ext.asyncio import AsyncSession

from app.application.models.metric import Metric
from app.application.protocols.database import MetricDatabaseGateway


class SQLMetricDatabaseGateway(MetricDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_train_metrics(self, model_id: int) -> list[Metric]:
        raise NotImplementedError

    async def get_eval_metrics(self, eval_model_id: int) -> list[Metric]:
        raise NotImplementedError
