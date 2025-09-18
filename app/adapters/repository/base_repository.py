from typing import Any, Generic, TypeVar
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import asc, desc, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query
from app.adapters.dto.pagination_dto import Pagination
from app.core.app_exception_response import AppExceptionResponse

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Базовый репозиторий для CRUD-операций."""

    def __init__(self, model: type[T], db: AsyncSession) -> None:
        self.model = model
        self.db = db

    async def get(
        self,
        id: int,
        options: list[Any] | None = None,
        include_deleted_filter: bool = False,
    ) -> T | None:
        """Получение объекта по ID."""
        filters = [self.model.id == id]
        filters = self._apply_soft_delete_filter(filters, include_deleted_filter)
        query = select(self.model).filter(*filters)
        if options:
            query = query.options(*options)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all(
        self,
        filters: list[Any] | None = None,
        options: list[Any] | None = None,
        order_by: str | None = None,
        order_direction: str = "asc",
        include_deleted_filter: bool = False,
    ) -> list[T]:
        """Получение всех объектов с поддержкой сортировки."""
        filters = self._apply_soft_delete_filter(filters, include_deleted_filter)
        query = select(self.model).filter(*filters)
        if options:
            query = query.options(*options)
        if order_by:
            query = self._apply_order_by(query, order_by, order_direction)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_with_filters(
        self,
        filters: list[Any],
        options: list[Any] | None = None,
        order_by: str | None = None,
        order_direction: str = "asc",
        include_deleted_filter: bool = False,
    ) -> list[T]:
        """Получение объектов с фильтрацией и сортировкой."""
        filters = self._apply_soft_delete_filter(filters, include_deleted_filter)
        query = select(self.model).filter(*filters)
        if options:
            query = query.options(*options)
        if order_by:
            query = self._apply_order_by(query, order_by, order_direction)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_first_with_filters(
        self,
        filters: list[Any],
        options: list[Any] | None = None,
        order_by: str | None = None,
        order_direction: str = "asc",
        include_deleted_filter: bool = False,
    ) -> T | None:
        """Получение первого объекта с фильтрацией."""
        filters = self._apply_soft_delete_filter(filters, include_deleted_filter)
        query = select(self.model).filter(*filters)
        if options:
            query = query.options(*options)
        if order_by:
            query = self._apply_order_by(query, order_by, order_direction)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def paginate(
        self,
        dto: BaseModel,
        page: int = 1,
        per_page: int = 20,
        filters: list[Any] | None = None,
        options: list[Any] | None = None,
        order_by: str | None = None,
        order_direction: str = "asc",
        include_deleted_filter: bool = False,
    ) -> Pagination:
        """Пагинация объектов с фильтрацией и сортировкой."""
        filters = self._apply_soft_delete_filter(filters, include_deleted_filter)
        query = select(self.model).filter(*filters)
        if options:
            query = query.options(*options)
        if order_by:
            query = self._apply_order_by(query, order_by, order_direction)

        total_items = await self.db.scalar(
            select(func.count()).select_from(query.subquery())
        )
        total_pages = (total_items + per_page - 1) // per_page

        results = await self.db.execute(
            query.limit(per_page).offset((page - 1) * per_page)
        )
        items = results.scalars().all()
        dto_items = [dto.from_orm(item) for item in items]

        return Pagination(
            items=dto_items,
            per_page=per_page,
            page=page,
            total_pages=total_pages,
            total_items=total_items,
        )

    async def create(self, obj: T) -> T:
        """Создание объекта."""
        try:
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError(self._parse_integrity_error(e))

    async def update(self, obj: T, dto: BaseModel | dict) -> T:
        """Обновление объекта."""
        try:
            if isinstance(dto, dict):
                data = dto
            else:
                # Поддержка как Pydantic v1 (.dict()), так и v2 (.model_dump())
                data = dto.model_dump(exclude_unset=True) if hasattr(dto, 'model_dump') else dto.dict(exclude_unset=True)

            for field, value in data.items():
                if hasattr(obj, field):
                    setattr(obj, field, value)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError(self._parse_integrity_error(e))

    async def delete(self, id: int, force_delete: bool = False) -> bool:
        """Удаление объекта. Если есть поле deleted_at — мягкое удаление."""
        obj = await self.get(id, include_deleted_filter=True)
        if not obj:
            raise AppExceptionResponse.not_found(message="Не найдено")

        if hasattr(obj, "deleted_at") and not force_delete:
            setattr(obj, "deleted_at", datetime.utcnow())
        else:
            await self.db.delete(obj)

        await self.db.commit()
        return True

    async def count(
        self, filters: list[Any] | None = None, include_deleted_filter: bool = False
    ) -> int:
        """Подсчёт количества записей с фильтрацией (или без)."""
        filters = self._apply_soft_delete_filter(filters, include_deleted_filter)
        query = select(func.count()).select_from(self.model).filter(*filters)
        result = await self.db.execute(query)
        return result.scalar() or 0

    def _parse_integrity_error(self, error: IntegrityError) -> str:
        """Парсинг ошибок уникальности."""
        orig_msg = str(error.orig)
        return f"IntegrityError: {orig_msg.split(':')[-1].strip()}"

    def _apply_order_by(
        self, query: Query, order_by: str, order_direction: str
    ) -> Query:
        """Применяет сортировку к запросу."""
        if order_direction.lower() == "desc":
            return query.order_by(desc(getattr(self.model, order_by)))
        return query.order_by(asc(getattr(self.model, order_by)))

    def _apply_soft_delete_filter(
        self, filters: list[Any] | None, include_deleted_filter: bool = False
    ) -> list[Any]:
        """Добавляет фильтр по deleted_at, если включен и поле существует."""
        if include_deleted_filter is False and hasattr(self.model, "deleted_at"):
            filters = filters or []
            filters.append(self.model.deleted_at.is_(None))
        return filters

    def default_relationships(self) -> list[Any]:
        """Определяет список стандартных подгружаемых связей."""
        return []
