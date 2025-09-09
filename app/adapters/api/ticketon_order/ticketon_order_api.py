from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.ticketon_order.ticketon_order_dto import (
    TicketonOrderRDTO,
    TicketonOrderWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import PaginationTicketonOrderWithRelationsRDTO
from app.adapters.filters.ticketon_order.ticketon_order_filter import TicketonOrderFilter
from app.adapters.filters.ticketon_order.ticketon_order_pagination_filter import TicketonOrderPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.route_constants import RoutePathConstants
from app.use_case.ticketon_order.all_ticketon_order_case import AllTicketonOrderCase
from app.use_case.ticketon_order.get_ticketon_order_by_id_case import GetTicketonOrderByIdCase
from app.use_case.ticketon_order.paginate_ticketon_order_case import PaginateTicketonOrderCase


class TicketonOrderApi:
    """
    API класс для управления заказами Ticketon.
    
    Предоставляет REST API эндпоинты для операций чтения заказов Ticketon.
    Включает операции: получение всех, получение по ID, пагинация.
    
    Примечание: Данный API предоставляет только операции чтения (All, Get, Paginate)
    для административного доступа к заказам Ticketon.
    """

    def __init__(self) -> None:
        """
        Инициализация TicketonOrderApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API заказов Ticketon.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """
        Регистрирует все маршруты API для заказов Ticketon.
        """
        self.router.get(
            f"{RoutePathConstants.IndexPathName}",
            response_model=PaginationTicketonOrderWithRelationsRDTO,
            summary="Пагинация заказов Ticketon",
            description="Получение пагинированного списка заказов Ticketon с отношениями",
        )(self.paginate)
        
        self.router.get(
            f"{RoutePathConstants.AllPathName}",
            response_model=list[TicketonOrderRDTO],
            summary="Список всех заказов Ticketon",
            description="Получение полного списка заказов Ticketon",
        )(self.get_all)
        
        self.router.get(
            f"{RoutePathConstants.GetByIdPathName}",
            response_model=TicketonOrderRDTO,
            summary="Получить заказ Ticketon по ID",
            description="Получение заказа Ticketon по уникальному идентификатору",
        )(self.get)

    async def paginate(
        self,
        filter: TicketonOrderPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationTicketonOrderWithRelationsRDTO:
        """
        Получение пагинированного списка заказов Ticketon с отношениями.
        
        Args:
            filter: Фильтр для пагинации с параметрами сортировки и поиска
            db: Сессия базы данных
            
        Returns:
            Пагинированный список заказов с отношениями
        """
        try:
            return await PaginateTicketonOrderCase(db).execute(filter=filter)
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
        filter: TicketonOrderFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[TicketonOrderRDTO]:
        """
        Получение полного списка заказов Ticketon.
        
        Args:
            filter: Фильтр для поиска и сортировки
            db: Сессия базы данных
            
        Returns:
            Список всех заказов Ticketon
        """
        try:
            return await AllTicketonOrderCase(db).execute(filter=filter)
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
    ) -> TicketonOrderRDTO:
        """
        Получение заказа Ticketon по ID.
        
        Args:
            id: Уникальный идентификатор заказа
            db: Сессия базы данных
            
        Returns:
            Найденный заказ Ticketon
        """
        try:
            return await GetTicketonOrderByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc