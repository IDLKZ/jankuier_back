from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.ticketon_order.ticketon_order_dto import (
    TicketonOrderRDTO,
    TicketonOrderWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import PaginationTicketonOrderWithRelationsRDTO
from app.adapters.dto.ticketon.ticketon_booking_dto import TicketonBookingRequestDTO
from app.adapters.dto.ticketon.ticketon_response_for_sale_dto import TicketonResponseForSaleDTO
from app.adapters.filters.ticketon_order.ticketon_order_filter import TicketonOrderFilter
from app.adapters.filters.ticketon_order.ticketon_order_pagination_filter import TicketonOrderPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.route_constants import RoutePathConstants
from app.use_case.ticketon_order.all_ticketon_order_case import AllTicketonOrderCase
from app.use_case.ticketon_order.get_ticketon_order_by_id_case import GetTicketonOrderByIdCase
from app.use_case.ticketon_order.paginate_ticketon_order_case import PaginateTicketonOrderCase
from app.use_case.ticketon_order.client.create_sale_case import CreateSaleTicketonAndOrderCase
from app.use_case.ticketon_order.client.recreate_payment_case import RecreatePaymentForTicketonOrderCase


class TicketonOrderApi:
    """
    API класс для управления заказами Ticketon.
    
    Предоставляет REST API эндпоинты для операций с заказами Ticketon.
    Включает операции: получение всех, получение по ID, пагинация, создание продажи.
    
    Примечание: Данный API предоставляет операции чтения (All, Get, Paginate)
    и создания продажи билетов через Ticketon API.
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
        
        self.router.post(
            "/create-sale",
            response_model=TicketonResponseForSaleDTO,
            summary="Создать продажу билетов Ticketon",
            description="Создание заказа и транзакции оплаты для покупки билетов через Ticketon API",
        )(self.create_sale)
        
        self.router.post(
            "/recreate-payment/{ticketon_order_id}",
            response_model=TicketonResponseForSaleDTO,
            summary="Пересоздать платеж для заказа Ticketon",
            description="Находит активную транзакцию или создает новую для существующего заказа Ticketon",
        )(self.recreate_payment)

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

    async def create_sale(
        self,
        dto: TicketonBookingRequestDTO,
        db: AsyncSession = Depends(get_db),
    ) -> TicketonResponseForSaleDTO:
        """
        Создание продажи билетов через Ticketon API.
        
        Создаёт заказ в системе Ticketon, формирует транзакцию оплаты в Alatau
        и связывает их между собой. Без авторизации пользователя.
        
        Args:
            dto: Данные для создания заказа (показ, билеты, контактная информация)
            db: Сессия базы данных
            
        Returns:
            Ответ с данными заказа Ticketon, транзакции оплаты и ID платежа
        """
        try:
            return await CreateSaleTicketonAndOrderCase(db).execute(dto=dto, user=None)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def recreate_payment(
        self,
        ticketon_order_id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> TicketonResponseForSaleDTO:
        """
        Пересоздание/восстановление платежа для существующего заказа Ticketon.
        
        Находит активную payment_transaction для заказа или создает новую.
        Логика:
        1. Проверяет существование и валидность заказа Ticketon
        2. Ищет активную payment_transaction (is_active=True, is_paid=False, is_canceled=False, не истекшая)
        3. Если активная найдена - возвращает её данные
        4. Если не найдена - создает новую payment_transaction
        5. Деактивирует старые транзакции
        
        Args:
            ticketon_order_id: ID заказа Ticketon
            db: Сессия базы данных
            
        Returns:
            TicketonResponseForSaleDTO с данными для оплаты
        """
        try:
            return await RecreatePaymentForTicketonOrderCase(db).execute(
                ticketon_order_id=ticketon_order_id
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc