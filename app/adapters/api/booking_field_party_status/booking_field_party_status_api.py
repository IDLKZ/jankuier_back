from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.booking_field_party_status.booking_field_party_status_dto import (
    BookingFieldPartyStatusCDTO,
    BookingFieldPartyStatusWithRelationsRDTO,
)
from app.adapters.filters.booking_field_party_status.booking_field_party_status_filter import BookingFieldPartyStatusFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.booking_field_party_status.all_booking_field_party_status_case import AllBookingFieldPartyStatusCase
from app.use_case.booking_field_party_status.create_booking_field_party_status_case import CreateBookingFieldPartyStatusCase
from app.use_case.booking_field_party_status.delete_booking_field_party_status_case import DeleteBookingFieldPartyStatusCase
from app.use_case.booking_field_party_status.get_booking_field_party_status_by_id_case import GetBookingFieldPartyStatusByIdCase
from app.use_case.booking_field_party_status.update_booking_field_party_status_case import UpdateBookingFieldPartyStatusCase


class BookingFieldPartyStatusApi:
    """
    API класс для управления статусами бронирования площадок.

    Предоставляет REST API эндпоинты для CRUD операций над статусами бронирования площадок.
    Включает стандартные операции: создание, чтение, обновление, удаление, получение списка.
    """

    def __init__(self) -> None:
        """
        Инициализация BookingFieldPartyStatusApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API статусов бронирования.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """
        Регистрирует все маршруты API для статусов бронирования площадок.
        """
        self.router.get(
            f"{RoutePathConstants.AllPathName}",
            response_model=list[BookingFieldPartyStatusWithRelationsRDTO],
            summary="Список всех статусов бронирования площадок",
            description="Получение полного списка статусов бронирования с relationships",
        )(self.get_all)

        self.router.post(
            f"{RoutePathConstants.CreatePathName}",
            response_model=BookingFieldPartyStatusWithRelationsRDTO,
            summary="Создать статус бронирования площадки",
            description="Создание нового статуса бронирования площадки",
        )(self.create)

        self.router.put(
            f"{RoutePathConstants.UpdatePathName}",
            response_model=BookingFieldPartyStatusWithRelationsRDTO,
            summary="Обновить статус бронирования площадки",
            description="Обновление статуса бронирования площадки по ID",
        )(self.update)

        self.router.get(
            f"{RoutePathConstants.GetByIdPathName}",
            response_model=BookingFieldPartyStatusWithRelationsRDTO,
            summary="Получить статус бронирования площадки по ID",
            description="Получение статуса бронирования по уникальному идентификатору с relationships",
        )(self.get)

        self.router.delete(
            f"{RoutePathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалить статус бронирования площадки",
            description="Удаление статуса бронирования площадки по ID",
        )(self.delete)

    async def get_all(
        self,
        filter: BookingFieldPartyStatusFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[BookingFieldPartyStatusWithRelationsRDTO]:
        """
        Получение полного списка статусов бронирования площадок.

        Args:
            filter: Фильтр для поиска и сортировки
            db: Сессия базы данных

        Returns:
            Список всех статусов бронирования с relationships
        """
        try:
            return await AllBookingFieldPartyStatusCase(db).execute(filter=filter)
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
        dto: BookingFieldPartyStatusCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> BookingFieldPartyStatusWithRelationsRDTO:
        """
        Создание нового статуса бронирования площадки.

        Args:
            dto: DTO с данными для создания статуса
            db: Сессия базы данных

        Returns:
            Созданный статус бронирования с relationships
        """
        try:
            return await CreateBookingFieldPartyStatusCase(db).execute(dto=dto)
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
        dto: BookingFieldPartyStatusCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> BookingFieldPartyStatusWithRelationsRDTO:
        """
        Обновление статуса бронирования площадки.

        Args:
            id: Уникальный идентификатор статуса
            dto: DTO с обновленными данными
            db: Сессия базы данных

        Returns:
            Обновленный статус бронирования с relationships
        """
        try:
            return await UpdateBookingFieldPartyStatusCase(db).execute(id=id, dto=dto)
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
    ) -> BookingFieldPartyStatusWithRelationsRDTO:
        """
        Получение статуса бронирования площадки по ID.

        Args:
            id: Уникальный идентификатор статуса
            db: Сессия базы данных

        Returns:
            Найденный статус бронирования с relationships
        """
        try:
            return await GetBookingFieldPartyStatusByIdCase(db).execute(id=id)
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
        Удаление статуса бронирования площадки.

        Args:
            id: Уникальный идентификатор статуса
            force_delete: Флаг принудительного удаления
            db: Сессия базы данных

        Returns:
            True если статус успешно удален
        """
        try:
            return await DeleteBookingFieldPartyStatusCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc