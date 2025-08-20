import logging
from abc import ABC, abstractmethod

from sqlalchemy import func, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.app_config import app_config

logger = logging.getLogger(__name__)


class BaseSeeder(ABC):
    """Базовый класс для всех сидеров."""

    def __init__(self) -> None:
        self.environment = (
            app_config.app_status
        )  # Получение текущего окружения (prod/dev)
        self.db_type = app_config.app_database

    @abstractmethod
    async def seed(self, session: AsyncSession) -> None:
        """Метод для заполнения базы данных."""

    def get_data(self):  # noqa:ANN204,ANN201,RUF100,RUF100
        """Загрузка данных в зависимости от окружения."""
        if self.environment == "production":
            return self.get_prod_data()
        return self.get_dev_data()

    def get_updated_data(self):  # noqa:ANN204,ANN201,RUF100
        """Загрузка данных в зависимости от окружения."""
        if self.environment == "production":
            return self.get_prod_updated_data()
        return self.get_dev_updated_data()

    @abstractmethod
    def get_dev_data(self):  # noqa:ANN204,ANN201,RUF100
        """Возвращает данные для разработки."""

    @abstractmethod
    def get_prod_data(self):  # noqa:ANN204,ANN201,RUF100
        """Возвращает данные для продакшена."""

    @abstractmethod
    def get_dev_updated_data(self):  # noqa:ANN204,ANN201,RUF100
        """Возвращает данные для разработки."""

    @abstractmethod
    def get_prod_updated_data(self):  # noqa:ANN204,ANN201,RUF100
        """Возвращает данные для продакшена."""

    async def reset_sequence(self, session: AsyncSession, table_name: str) -> None:
        if self.db_type.startswith("postgresql"):
            await session.execute(
                text(
                    f"""
                       DO $$
                       BEGIN
                           IF EXISTS (SELECT 1 FROM {table_name}) THEN
                               PERFORM setval(pg_get_serial_sequence('{table_name}', 'id'), MAX(id)) FROM {table_name};
                           ELSE
                               PERFORM setval(pg_get_serial_sequence('{table_name}', 'id'), 1, false);
                           END IF;
                       END
                       $$;
                   """  # noqa:S608
                )
            )

    async def load_seeders(
        self,
        BaseModel,  # noqa:N803,ANN001
        session,  # noqa:ANN001
        table_name: str,
        ready_data: list | None = None,
    ) -> None:
        # Проверяем, есть ли данные в таблице
        count_query = select(func.count()).select_from(BaseModel)
        total_items = await session.scalar(count_query)

        if total_items > 0:
            msg = f"Таблица {table_name} уже содержит данные ({total_items} записей)."
            logger.info(msg=msg)
            return

        # Добавляем данные, если они переданы
        if ready_data:
            session.add_all(ready_data)
            await session.commit()

            # Сбрасываем последовательность для PostgreSQL
            await self.reset_sequence(session, table_name)

    async def update_seeders(
        self,
        BaseModel,  # noqa:N803,ANN001
        session: AsyncSession,
        table_name: str,
        identification: str,
        update_data: list,  # Это список объектов или словарей
        add_if_not_exists: bool = False,
    ) -> None:
        """
        Обновление данных в таблице.

        Args:
            BaseModel: SQLAlchemy модель таблицы.
            session: Активная асинхронная сессия.
            table_name: Имя таблицы (для логирования).
            identification: Поле для идентификации записи (например, 'id' или 'value').
            update_data: Список записей для обновления/добавления.
            add_if_not_exists: Если True, добавляет новые записи, если их не существует.
        """
        if not update_data:
            msg = f"Нет данных для обновления/добавления в таблицу {table_name}."
            logger.info(msg)
            return

        for record in update_data:
            # Получаем идентификатор записи
            identifier = record.get(identification)
            if identifier is None:
                msg = f"Каждая запись должна содержать поле '{identification}' для идентификации."
                raise ValueError(msg)

            # Поиск существующей записи в базе данных
            stmt = select(BaseModel).where(
                getattr(BaseModel, identification) == identifier
            )
            result = await session.execute(stmt)
            existing_record = result.scalar_one_or_none()

            if existing_record:
                # Формируем данные для обновления только с изменёнными значениями
                update_fields = {
                    key: value
                    for key, value in record.items()
                    if key != identification
                    and getattr(existing_record, key, None) != value
                }
                if update_fields:
                    update_stmt = (
                        update(BaseModel)
                        .where(getattr(BaseModel, identification) == identifier)
                        .values(**update_fields)
                    )
                    await session.execute(update_stmt)
            elif add_if_not_exists:
                # Добавляем новую запись
                new_record = BaseModel(**record)
                session.add(new_record)

        await session.commit()
        msg = f"Данные успешно обновлены/добавлены в таблицу {table_name}."
        logger.info(msg)
