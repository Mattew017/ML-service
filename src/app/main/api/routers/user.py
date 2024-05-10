from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import Form, Depends, HTTPException, status
from fastapi.routing import APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.adapters.gateways.user import SQLUserDatabaseGateway
from app.application.models.user import User, UserRoleEnum
from app.application.protocols.database import UoW, UserDatabaseGateway
from app.main.settings import settings

user_router = APIRouter(prefix='/user', tags=['user'], route_class=DishkaRoute)

pwd_context = CryptContext(schemes=["bcrypt"])
security = HTTPBasic()

async_engine = create_async_engine(settings.db_uri)
session_maker = async_sessionmaker(async_engine, expire_on_commit=False, autoflush=False)


async def get_session() -> AsyncSession:
    async with session_maker() as session:
        yield session


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


async def get_auth_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                        session: AsyncSession = Depends(get_session),
                        ) -> User:
    user_gateway = SQLUserDatabaseGateway(session)
    unauthorized_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                       detail="Incorrect username or password",
                                       headers={"WWW-Authenticate": "Basic"})
    user = await user_gateway.get_by_username(credentials.username)
    if not user:
        raise unauthorized_error
    if not verify_password(credentials.password, user.password):
        raise unauthorized_error

    return user


async def get_current_username(user: User = Depends(get_auth_user)) -> str:
    return user.username


async def get_current_user_id(user: User = Depends(get_auth_user)) -> int:
    return user.id


@user_router.post('/register')
async def register_user(
        uow: FromDishka[UoW],
        user_gateway: FromDishka[UserDatabaseGateway],
        username: str = Form(...),
        password: str = Form(...)) -> int:
    if await user_gateway.get_by_username(username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    role = UserRoleEnum.USER
    password_hash = get_password_hash(password)
    user = User(username=username, password=password_hash, role=role, id=0)
    user_id = await user_gateway.add_user(user)
    await uow.commit()
    return user_id


@user_router.get('/login')
async def login_user(username: str = Depends(get_current_username)) -> str:
    return f'Hello, {username!r}!'


@user_router.get('/all')
async def get_all_users(user_gateway: FromDishka[UserDatabaseGateway]) -> list[User]:
    all_users = await user_gateway.get_all_users()

    return all_users
