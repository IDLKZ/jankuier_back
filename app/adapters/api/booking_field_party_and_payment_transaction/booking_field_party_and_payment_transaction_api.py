from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_dto import (
    BookingFieldPartyAndPaymentTransactionCDTO,
    BookingFieldPartyAndPaymentTransactionWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import PaginationBookingFieldPartyAndPaymentTransactionWithRelationsRDTO
from app.adapters.filters.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_pagination_filter import BookingFieldPartyAndPaymentTransactionPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.booking_field_party_and_payment_transaction.create_booking_field_party_and_payment_transaction_case import CreateBookingFieldPartyAndPaymentTransactionCase
from app.use_case.booking_field_party_and_payment_transaction.delete_booking_field_party_and_payment_transaction_case import DeleteBookingFieldPartyAndPaymentTransactionCase
from app.use_case.booking_field_party_and_payment_transaction.get_booking_field_party_and_payment_transaction_by_id_case import GetBookingFieldPartyAndPaymentTransactionByIdCase
from app.use_case.booking_field_party_and_payment_transaction.paginate_booking_field_party_and_payment_transaction_case import PaginateBookingFieldPartyAndPaymentTransactionCase
from app.use_case.booking_field_party_and_payment_transaction.update_booking_field_party_and_payment_transaction_case import UpdateBookingFieldPartyAndPaymentTransactionCase


class BookingFieldPartyAndPaymentTransactionApi:
    """
    API класс для управления связями между бронированиями площадок и платежными транзакциями.

    Предоставляет REST API эндпоинты для CRUD операций над связями бронирований и транзакций.
    Используется для отслеживания множественных попыток оплаты, перевыставленных счетов и возвратов.
    Включает стандартные операции: создание, чтение, обновление, удаление, пагинация.
    """

    def __init__(self) -> None:
        """
        Инициализация BookingFieldPartyAndPaymentTransactionApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API связей.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """
        Регистрирует все маршруты API для связей между бронированиями и транзакциями.
        """
        self.router.get(
            f"{RoutePathConstants.IndexPathName}",
            response_model=PaginationBookingFieldPartyAndPaymentTransactionWithRelationsRDTO,
            summary="Пагинация связей бронирований и транзакций",
            description="Получение пагинированного списка связей с relationships",
        )(self.paginate)

        self.router.post(
            f"{RoutePathConstants.CreatePathName}",
            response_model=BookingFieldPartyAndPaymentTransactionWithRelationsRDTO,
            summary="Создать связь между бронированием и транзакцией",
            description="Создание новой связи между бронированием площадки и платежной транзакцией",
        )(self.create)

        self.router.put(
            f"{RoutePathConstants.UpdatePathName}",
            response_model=BookingFieldPartyAndPaymentTransactionWithRelationsRDTO,
            summary="Обновить связь между бронированием и транзакцией",
            description="Обновление связи по ID (изменение типа, активности, флага основной транзакции)",
        )(self.update)

        self.router.get(
            f"{RoutePathConstants.GetByIdPathName}",
            response_model=BookingFieldPartyAndPaymentTransactionWithRelationsRDTO,
            summary="Получить связь по ID",
            description="Получение связи между бронированием и транзакцией по уникальному идентификатору с relationships",
        )(self.get)

        self.router.delete(
            f"{RoutePathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалить связь между бронированием и транзакцией",
            description="Удаление связи по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: BookingFieldPartyAndPaymentTransactionPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationBookingFieldPartyAndPaymentTransactionWithRelationsRDTO:
        """
        Получение пагинированного списка связей между бронированиями и транзакциями.

        Args:
            filter: Фильтр для пагинации с параметрами сортировки и поиска
            db: Сессия базы данных

        Returns:
            Пагинированный список связей с relationships (booking_request, payment_transaction)
        """
        try:
            return await PaginateBookingFieldPartyAndPaymentTransactionCase(db).execute(filter=filter)
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
        dto: BookingFieldPartyAndPaymentTransactionCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> BookingFieldPartyAndPaymentTransactionWithRelationsRDTO:
        """
        Создание новой связи между бронированием и транзакцией.

        Args:
            dto: DTO с данными для создания связи (request_id, payment_transaction_id, link_type, etc.)
            db: Сессия базы данных

        Returns:
            Созданная связь с relationships
        """
        try:
            return await CreateBookingFieldPartyAndPaymentTransactionCase(db).execute(dto=dto)
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
        dto: BookingFieldPartyAndPaymentTransactionCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> BookingFieldPartyAndPaymentTransactionWithRelationsRDTO:
        """
        Обновление связи между бронированием и транзакцией.

        Args:
            id: Уникальный идентификатор связи
            dto: DTO с обновленными данными (is_active, is_primary, link_type, link_reason)
            db: Сессия базы данных

        Returns:
            Обновленная связь с relationships
        """
        try:
            return await UpdateBookingFieldPartyAndPaymentTransactionCase(db).execute(id=id, dto=dto)
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
    ) -> BookingFieldPartyAndPaymentTransactionWithRelationsRDTO:
        """
        Получение связи между бронированием и транзакцией по ID.

        Args:
            id: Уникальный идентификатор связи
            db: Сессия базы данных

        Returns:
            Найденная связь с relationships (booking_request, payment_transaction)
        """
        try:
            return await GetBookingFieldPartyAndPaymentTransactionByIdCase(db).execute(id=id)
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
        Удаление связи между бронированием и транзакцией.

        Args:
            id: Уникальный идентификатор связи
            force_delete: Флаг принудительного удаления (hard delete)
            db: Сессия базы данных

        Returns:
            True если связь успешно удалена
        """
        try:
            return await DeleteBookingFieldPartyAndPaymentTransactionCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc