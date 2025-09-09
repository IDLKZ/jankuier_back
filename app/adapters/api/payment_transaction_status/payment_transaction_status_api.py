from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.payment_transaction_status.payment_transaction_status_dto import (
    PaymentTransactionStatusRDTO,
    PaymentTransactionStatusCDTO,
    PaymentTransactionStatusWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import PaginationPaymentTransactionStatusWithRelationsRDTO
from app.adapters.filters.payment_transaction_status.payment_transaction_status_filter import PaymentTransactionStatusFilter
from app.adapters.filters.payment_transaction_status.payment_transaction_status_pagination_filter import PaymentTransactionStatusPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.payment_transaction_status.all_payment_transaction_status_case import AllPaymentTransactionStatusCase
from app.use_case.payment_transaction_status.create_payment_transaction_status_case import CreatePaymentTransactionStatusCase
from app.use_case.payment_transaction_status.delete_payment_transaction_status_case import DeletePaymentTransactionStatusCase
from app.use_case.payment_transaction_status.get_payment_transaction_status_by_id_case import GetPaymentTransactionStatusByIdCase
from app.use_case.payment_transaction_status.paginate_payment_transaction_status_case import PaginatePaymentTransactionStatusCase
from app.use_case.payment_transaction_status.update_payment_transaction_status_case import UpdatePaymentTransactionStatusCase


class PaymentTransactionStatusApi:
    """
    API класс для управления статусами платежных транзакций.
    
    Предоставляет REST API эндпоинты для CRUD операций над статусами платежных транзакций.
    Включает стандартные операции: создание, чтение, обновление, удаление, пагинация.
    """

    def __init__(self) -> None:
        """
        Инициализация PaymentTransactionStatusApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API статусов платежных транзакций.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """
        Регистрирует все маршруты API для статусов платежных транзакций.
        """
        self.router.get(
            f"{RoutePathConstants.IndexPathName}",
            response_model=PaginationPaymentTransactionStatusWithRelationsRDTO,
            summary="Пагинация статусов платежных транзакций",
            description="Получение пагинированного списка статусов платежных транзакций с отношениями",
        )(self.paginate)
        
        self.router.get(
            f"{RoutePathConstants.AllPathName}",
            response_model=list[PaymentTransactionStatusRDTO],
            summary="Список всех статусов платежных транзакций",
            description="Получение полного списка статусов платежных транзакций",
        )(self.get_all)
        
        self.router.post(
            f"{RoutePathConstants.CreatePathName}",
            response_model=PaymentTransactionStatusRDTO,
            summary="Создать статус платежной транзакции",
            description="Создание нового статуса платежной транзакции",
        )(self.create)
        
        self.router.put(
            f"{RoutePathConstants.UpdatePathName}",
            response_model=PaymentTransactionStatusRDTO,
            summary="Обновить статус платежной транзакции",
            description="Обновление статуса платежной транзакции по ID",
        )(self.update)
        
        self.router.get(
            f"{RoutePathConstants.GetByIdPathName}",
            response_model=PaymentTransactionStatusRDTO,
            summary="Получить статус платежной транзакции по ID",
            description="Получение статуса платежной транзакции по уникальному идентификатору",
        )(self.get)
        
        self.router.delete(
            f"{RoutePathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалить статус платежной транзакции",
            description="Удаление статуса платежной транзакции по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: PaymentTransactionStatusPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationPaymentTransactionStatusWithRelationsRDTO:
        """
        Получение пагинированного списка статусов платежных транзакций с отношениями.
        
        Args:
            filter: Фильтр для пагинации с параметрами сортировки и поиска
            db: Сессия базы данных
            
        Returns:
            Пагинированный список статусов с отношениями
        """
        try:
            return await PaginatePaymentTransactionStatusCase(db).execute(filter=filter)
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
        filter: PaymentTransactionStatusFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[PaymentTransactionStatusRDTO]:
        """
        Получение полного списка статусов платежных транзакций.
        
        Args:
            filter: Фильтр для поиска и сортировки
            db: Сессия базы данных
            
        Returns:
            Список всех статусов платежных транзакций
        """
        try:
            return await AllPaymentTransactionStatusCase(db).execute(filter=filter)
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
        dto: PaymentTransactionStatusCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> PaymentTransactionStatusRDTO:
        """
        Создание нового статуса платежной транзакции.
        
        Args:
            dto: DTO с данными для создания статуса
            db: Сессия базы данных
            
        Returns:
            Созданный статус платежной транзакции
        """
        try:
            return await CreatePaymentTransactionStatusCase(db).execute(dto=dto)
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
        dto: PaymentTransactionStatusCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> PaymentTransactionStatusRDTO:
        """
        Обновление статуса платежной транзакции.
        
        Args:
            id: Уникальный идентификатор статуса
            dto: DTO с обновленными данными
            db: Сессия базы данных
            
        Returns:
            Обновленный статус платежной транзакции
        """
        try:
            return await UpdatePaymentTransactionStatusCase(db).execute(id=id, dto=dto)
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
    ) -> PaymentTransactionStatusRDTO:
        """
        Получение статуса платежной транзакции по ID.
        
        Args:
            id: Уникальный идентификатор статуса
            db: Сессия базы данных
            
        Returns:
            Найденный статус платежной транзакции
        """
        try:
            return await GetPaymentTransactionStatusByIdCase(db).execute(id=id)
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
        Удаление статуса платежной транзакции.
        
        Args:
            id: Уникальный идентификатор статуса
            force_delete: Флаг принудительного удаления
            db: Сессия базы данных
            
        Returns:
            True если статус успешно удален
        """
        try:
            return await DeletePaymentTransactionStatusCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc