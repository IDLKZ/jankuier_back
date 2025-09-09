from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.ticketon_order_status.ticketon_order_status_dto import (
    TicketonOrderStatusRDTO,
    TicketonOrderStatusCDTO,
    TicketonOrderStatusWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import PaginationTicketonOrderStatusWithRelationsRDTO
from app.adapters.filters.ticketon_order_status.ticketon_order_status_filter import TicketonOrderStatusFilter
from app.adapters.filters.ticketon_order_status.ticketon_order_status_pagination_filter import TicketonOrderStatusPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.ticketon_order_status.all_ticketon_order_status_case import AllTicketonOrderStatusCase
from app.use_case.ticketon_order_status.create_ticketon_order_status_case import CreateTicketonOrderStatusCase
from app.use_case.ticketon_order_status.delete_ticketon_order_status_case import DeleteTicketonOrderStatusCase
from app.use_case.ticketon_order_status.get_ticketon_order_status_by_id_case import GetTicketonOrderStatusByIdCase
from app.use_case.ticketon_order_status.paginate_ticketon_order_status_case import PaginateTicketonOrderStatusCase
from app.use_case.ticketon_order_status.update_ticketon_order_status_case import UpdateTicketonOrderStatusCase


class TicketonOrderStatusApi:
    """
    API класс для управления статусами заказов Ticketon.
    
    Предоставляет REST API эндпоинты для CRUD операций над статусами заказов Ticketon.
    Включает стандартные операции: создание, чтение, обновление, удаление, пагинация.
    """

    def __init__(self) -> None:
        """
        Инициализация TicketonOrderStatusApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API статусов заказов Ticketon.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """
        Регистрирует все маршруты API для статусов заказов Ticketon.
        """
        self.router.get(
            f"{RoutePathConstants.IndexPathName}",
            response_model=PaginationTicketonOrderStatusWithRelationsRDTO,
            summary="Пагинация статусов заказов Ticketon",
            description="Получение пагинированного списка статусов заказов Ticketon с отношениями",
        )(self.paginate)
        
        self.router.get(
            f"{RoutePathConstants.AllPathName}",
            response_model=list[TicketonOrderStatusRDTO],
            summary="Список всех статусов заказов Ticketon",
            description="Получение полного списка статусов заказов Ticketon",
        )(self.get_all)
        
        self.router.post(
            f"{RoutePathConstants.CreatePathName}",
            response_model=TicketonOrderStatusRDTO,
            summary="Создать статус заказа Ticketon",
            description="Создание нового статуса заказа Ticketon",
        )(self.create)
        
        self.router.put(
            f"{RoutePathConstants.UpdatePathName}",
            response_model=TicketonOrderStatusRDTO,
            summary="Обновить статус заказа Ticketon",
            description="Обновление статуса заказа Ticketon по ID",
        )(self.update)
        
        self.router.get(
            f"{RoutePathConstants.GetByIdPathName}",
            response_model=TicketonOrderStatusRDTO,
            summary="Получить статус заказа Ticketon по ID",
            description="Получение статуса заказа Ticketon по уникальному идентификатору",
        )(self.get)
        
        self.router.delete(
            f"{RoutePathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалить статус заказа Ticketon",
            description="Удаление статуса заказа Ticketon по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: TicketonOrderStatusPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationTicketonOrderStatusWithRelationsRDTO:
        """
        Получение пагинированного списка статусов заказов Ticketon с отношениями.
        
        Args:
            filter: Фильтр для пагинации с параметрами сортировки и поиска
            db: Сессия базы данных
            
        Returns:
            Пагинированный список статусов с отношениями
        """
        try:
            return await PaginateTicketonOrderStatusCase(db).execute(filter=filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_all(
        self,
        filter: TicketonOrderStatusFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[TicketonOrderStatusRDTO]:
        """
        Получение полного списка статусов заказов Ticketon.
        
        Args:
            filter: Фильтр для поиска и сортировки
            db: Сессия базы данных
            
        Returns:
            Список всех статусов заказов Ticketon
        """
        try:
            return await AllTicketonOrderStatusCase(db).execute(filter=filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def create(
        self,
        dto: TicketonOrderStatusCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> TicketonOrderStatusRDTO:
        """
        Создание нового статуса заказа Ticketon.
        
        Args:
            dto: DTO с данными для создания статуса
            db: Сессия базы данных
            
        Returns:
            Созданный статус заказа Ticketon
        """
        try:
            return await CreateTicketonOrderStatusCase(db).execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def update(
        self,
        id: RoutePathConstants.IDPath,
        dto: TicketonOrderStatusCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> TicketonOrderStatusRDTO:
        """
        Обновление статуса заказа Ticketon.
        
        Args:
            id: Уникальный идентификатор статуса
            dto: DTO с обновленными данными
            db: Сессия базы данных
            
        Returns:
            Обновленный статус заказа Ticketon
        """
        try:
            return await UpdateTicketonOrderStatusCase(db).execute(id=id, dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get(
        self,
        id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> TicketonOrderStatusRDTO:
        """
        Получение статуса заказа Ticketon по ID.
        
        Args:
            id: Уникальный идентификатор статуса
            db: Сессия базы данных
            
        Returns:
            Найденный статус заказа Ticketon
        """
        try:
            return await GetTicketonOrderStatusByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def delete(
        self,
        id: RoutePathConstants.IDPath,
        force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        """
        Удаление статуса заказа Ticketon.
        
        Args:
            id: Уникальный идентификатор статуса
            force_delete: Флаг принудительного удаления
            db: Сессия базы данных
            
        Returns:
            True если статус успешно удален
        """
        try:
            return await DeleteTicketonOrderStatusCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc