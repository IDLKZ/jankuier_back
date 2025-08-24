from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.infrastructure.app_config import app_config

# 🎯 Создаём асинхронный движок SQLAlchemy
engine_async = create_async_engine(
    app_config.get_connection_url,
    echo=False,
    pool_size=app_config.db_pool_size,
    max_overflow=app_config.db_max_overflow,
    pool_timeout=app_config.db_pool_timeout,
    pool_recycle=app_config.db_pool_recycle,
)

engine_sync = create_engine(app_config.get_connection_sync_url())

# 🎯 Создаём фабрику сессий
AsyncSessionLocal = sessionmaker(
    bind=engine_async, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


"""📌 Синхронная версия get_db() для Celery"""


@contextmanager
def get_db_sync():  # noqa:ANN201
    session = AsyncSessionLocal()
    try:
        yield session  # 🔥 Используем yield
    finally:
        session.close()  # ✅ Гарантированно закрываем соединение


class Base(DeclarativeBase):
    """📌 Базовая модель"""
