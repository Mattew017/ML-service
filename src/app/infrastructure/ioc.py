from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
    provide,
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker

from app.adapters.gateways.dataset import SQLDatasetDatabaseGateway
from app.adapters.gateways.metric import SQLMetricDatabaseGateway
from app.adapters.gateways.model import SQLModelDatabaseGateway
from app.adapters.gateways.user import SQLUserDatabaseGateway
from app.adapters.unit_of_work import SQLUnitOfWork
from app.application.protocols.database import (UoW, UserDatabaseGateway,
                                                DatasetDatabaseGateway, ModelDatabaseGateway, MetricDatabaseGateway)
from app.main.settings import settings


class SQLSessionProvider(Provider):
    @provide(scope=Scope.APP, provides=AsyncEngine)
    async def provide_async_engine(self):
        return create_async_engine(settings.db_uri, echo=True)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_async_session(self, engine: AsyncEngine):
        async_session = async_sessionmaker(engine, expire_on_commit=False, autoflush=False, autocommit=False)
        session = async_session()
        yield session
        await session.close()


class DatabaseAdaptersProvider(Provider):
    scope = Scope.REQUEST

    unit_of_work = provide(SQLUnitOfWork, provides=UoW)
    user_gateway = provide(SQLUserDatabaseGateway, provides=UserDatabaseGateway)
    dataset_gateway = provide(SQLDatasetDatabaseGateway, provides=DatasetDatabaseGateway)
    model_gateway = provide(SQLModelDatabaseGateway, provides=ModelDatabaseGateway)
    metric_gateway = provide(SQLMetricDatabaseGateway, provides=MetricDatabaseGateway)


def create_container() -> AsyncContainer:
    return make_async_container(
        SQLSessionProvider(),
        DatabaseAdaptersProvider(),
    )
