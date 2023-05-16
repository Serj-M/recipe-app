from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
logger_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    """
    Return session
    """
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session
