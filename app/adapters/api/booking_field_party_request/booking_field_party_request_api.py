from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import (
    BookingFieldPartyRequestCDTO,
    BookingFieldPartyRequestWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import PaginationBookingFieldPartyRequestWithRelationsRDTO
from app.adapters.filters.booking_field_party_request.booking_field_party_request_pagination_filter import BookingFieldPartyRequestPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.booking_field_party_request.create_booking_field_party_request_case import CreateBookingFieldPartyRequestCase
from app.use_case.booking_field_party_request.delete_booking_field_party_request_case import DeleteBookingFieldPartyRequestCase
from app.use_case.booking_field_party_request.get_booking_field_party_request_by_id_case import GetBookingFieldPartyRequestByIdCase
from app.use_case.booking_field_party_request.paginate_booking_field_party_request_case import PaginateBookingFieldPartyRequestCase
from app.use_case.booking_field_party_request.update_booking_field_party_request_case import UpdateBookingFieldPartyRequestCase


class BookingFieldPartyRequestApi:
    """
    API класс для управления бронированиями площадок.

    Предоставляет REST API эндпоинты для CRUD операций над бронированиями площадок.
    Включает стандартные операции: создание, чтение, обновление, удаление, пагинация.
    """

    def __init__(self) -> None:
        """
        Инициализация BookingFieldPartyRequestApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API бронирований.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """
        Регистрирует все маршруты API для бронирований площадок.
        """
        self.router.get(
            f"{RoutePathConstants.IndexPathName}",
            response_model=PaginationBookingFieldPartyRequestWithRelationsRDTO,
            summary="Пагинация бронирований площадок",
            description="Получение пагинированного списка бронирований с relationships",
        )(self.paginate)

        self.router.post(
            f"{RoutePathConstants.CreatePathName}",
            response_model=BookingFieldPartyRequestWithRelationsRDTO,
            summary="Создать бронирование площадки",
            description="Создание нового бронирования площадки",
        )(self.create)

        self.router.put(
            f"{RoutePathConstants.UpdatePathName}",
            response_model=BookingFieldPartyRequestWithRelationsRDTO,
            summary="Обновить бронирование площадки",
            description="Обновление бронирования площадки по ID",
        )(self.update)

        self.router.get(
            f"{RoutePathConstants.GetByIdPathName}",
            response_model=BookingFieldPartyRequestWithRelationsRDTO,
            summary="Получить бронирование площадки по ID",
            description="Получение бронирования по уникальному идентификатору с relationships",
        )(self.get)

        self.router.delete(
            f"{RoutePathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалить бронирование площадки",
            description="Удаление бронирования площадки по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: BookingFieldPartyRequestPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationBookingFieldPartyRequestWithRelationsRDTO:
        """
        Получение пагинированного списка бронирований площадок с relationships.

        Args:
            filter: Фильтр для пагинации с параметрами сортировки и поиска
            db: Сессия базы данных

        Returns:
            Пагинированный список бронирований с relationships
        """
        try:
            return await PaginateBookingFieldPartyRequestCase(db).execute(filter=filter)
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
        dto: BookingFieldPartyRequestCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> BookingFieldPartyRequestWithRelationsRDTO:
        """
        Создание нового бронирования площадки.

        Args:
            dto: DTO с данными для создания бронирования
            db: Сессия базы данных

        Returns:
            Созданное бронирование с relationships
        """
        try:
            return await CreateBookingFieldPartyRequestCase(db).execute(dto=dto)
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
        dto: BookingFieldPartyRequestCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> BookingFieldPartyRequestWithRelationsRDTO:
        """
        Обновление бронирования площадки.

        Args:
            id: Уникальный идентификатор бронирования
            dto: DTO с обновленными данными
            db: Сессия базы данных

        Returns:
            Обновленное бронирование с relationships
        """
        try:
            return await UpdateBookingFieldPartyRequestCase(db).execute(id=id, dto=dto)
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
    ) -> BookingFieldPartyRequestWithRelationsRDTO:
        """
        Получение бронирования площадки по ID.

        Args:
            id: Уникальный идентификатор бронирования
            db: Сессия базы данных

        Returns:
            Найденное бронирование с relationships
        """
        try:
            return await GetBookingFieldPartyRequestByIdCase(db).execute(id=id)
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
        Удаление бронирования площадки.

        Args:
            id: Уникальный идентификатор бронирования
            force_delete: Флаг принудительного удаления
            db: Сессия базы данных

        Returns:
            True если бронирование успешно удалено
        """
        try:
            return await DeleteBookingFieldPartyRequestCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc