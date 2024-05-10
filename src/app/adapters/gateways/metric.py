from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.models.metric import Metric
from app.application.protocols.database import MetricDatabaseGateway
from app.adapters.models.metrics import MetricTable, EvaluationMetricsTable, TrainMetricsTable


class SQLMetricDatabaseGateway(MetricDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_train_metric(self, model_id: int, metric: Metric) -> None:
        metric_id = await self.session.execute(select(MetricTable).where(MetricTable.name == metric.name))
        metric_id = metric_id.scalars().first().id
        train_metric_obj = TrainMetricsTable(model_id=model_id, metric_id=metric_id, value=metric.value)
        self.session.add(train_metric_obj)

    async def add_eval_metric(self, eval_model_id: int, metric: Metric) -> None:
        metric_id = await self.session.execute(select(MetricTable).where(MetricTable.name == metric.name))
        metric_id = metric_id.scalars().first().id
        train_metric_obj = EvaluationMetricsTable(model_id=eval_model_id, metric_id=metric_id, value=metric.value)
        self.session.add(train_metric_obj)

    async def get_train_metrics(self, model_id: int) -> list[Metric]:
        stmt = (select(TrainMetricsTable).
                where(TrainMetricsTable.model_id == model_id)
                .join(MetricTable, TrainMetricsTable.metric_id == MetricTable.id))
        res = await self.session.execute(stmt)
        res = res.scalars().all()
        return [Metric(name=metric.metric.name, value=metric.value) for metric in res]

    async def get_eval_metrics(self, eval_model_id: int) -> list[Metric]:
        stmt = (select(EvaluationMetricsTable)
                .where(EvaluationMetricsTable.model_id == eval_model_id)
                .join(MetricTable, EvaluationMetricsTable.metric_id == MetricTable.id))

        res = await self.session.execute(stmt)
        res = res.scalars().all()
        return [Metric(name=metric.metric.name, value=metric.value) for metric in res]
