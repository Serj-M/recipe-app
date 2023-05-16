from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
logger_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    """
    Функция возвращает сессию для работы с БД.
    """
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session
