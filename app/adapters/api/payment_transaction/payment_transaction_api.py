from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.payment_transaction.payment_transaction_dto import (
    PaymentTransactionRDTO,
    PaymentTransactionWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import PaginationPaymentTransactionWithRelationsRDTO
from app.adapters.filters.payment_transaction.payment_transaction_filter import PaymentTransactionFilter
from app.adapters.filters.payment_transaction.payment_transaction_pagination_filter import PaymentTransactionPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.route_constants import RoutePathConstants
from app.use_case.payment_transaction.all_payment_transaction_case import AllPaymentTransactionCase
from app.use_case.payment_transaction.get_payment_transaction_by_id_case import GetPaymentTransactionByIdCase
from app.use_case.payment_transaction.paginate_payment_transaction_case import PaginatePaymentTransactionCase


class PaymentTransactionApi:
    """
    API класс для управления платежными транзакциями.
    
    Предоставляет REST API эндпоинты для операций чтения платежных транзакций.
    Включает операции: получение всех, получение по ID, пагинация.
    
    Примечание: Данный API предоставляет только операции чтения (All, Get, Paginate)
    для административного доступа к платежным транзакциям.
    """

    def __init__(self) -> None:
        """
        Инициализация PaymentTransactionApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API платежных транзакций.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """
        Регистрирует все маршруты API для платежных транзакций.
        """
        self.router.get(
            f"{RoutePathConstants.IndexPathName}",
            response_model=PaginationPaymentTransactionWithRelationsRDTO,
            summary="Пагинация платежных транзакций",
            description="Получение пагинированного списка платежных транзакций с отношениями",
        )(self.paginate)
        
        self.router.get(
            f"{RoutePathConstants.AllPathName}",
            response_model=list[PaymentTransactionRDTO],
            summary="Список всех платежных транзакций",
            description="Получение полного списка платежных транзакций",
        )(self.get_all)
        
        self.router.get(
            f"{RoutePathConstants.GetByIdPathName}",
            response_model=PaymentTransactionRDTO,
            summary="Получить платежную транзакцию по ID",
            description="Получение платежной транзакции по уникальному идентификатору",
        )(self.get)

    async def paginate(
        self,
        filter: PaymentTransactionPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationPaymentTransactionWithRelationsRDTO:
        """
        Получение пагинированного списка платежных транзакций с отношениями.
        
        Args:
            filter: Фильтр для пагинации с параметрами сортировки и поиска
            db: Сессия базы данных
            
        Returns:
            Пагинированный список транзакций с отношениями
        """
        try:
            return await PaginatePaymentTransactionCase(db).execute(filter=filter)
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
        filter: PaymentTransactionFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[PaymentTransactionRDTO]:
        """
        Получение полного списка платежных транзакций.
        
        Args:
            filter: Фильтр для поиска и сортировки
            db: Сессия базы данных
            
        Returns:
            Список всех платежных транзакций
        """
        try:
            return await AllPaymentTransactionCase(db).execute(filter=filter)
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
    ) -> PaymentTransactionRDTO:
        """
        Получение платежной транзакции по ID.
        
        Args:
            id: Уникальный идентификатор транзакции
            db: Сессия базы данных
            
        Returns:
            Найденная платежная транзакция
        """
        try:
            return await GetPaymentTransactionByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc