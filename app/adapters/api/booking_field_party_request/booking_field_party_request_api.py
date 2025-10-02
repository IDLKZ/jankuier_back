from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.alatau.alatau_after_payment_dto import AlatauBackrefGetDTO
from app.adapters.dto.booking_field_party_request.booking_field_party_create_request_dto import (
    CreateBookingFieldPartyRequestDTO,
    CreateBookingFieldPartyResponseDTO,
    AcceptPaymentForBookingFieldPartyResponseDTO
)
from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import (
    BookingFieldPartyRequestCDTO,
    BookingFieldPartyRequestWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import PaginationBookingFieldPartyRequestWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.filters.booking_field_party_request.booking_field_party_request_pagination_filter import BookingFieldPartyRequestPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.middleware.role_middleware import check_client
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.booking_field_party_request.client.accept_payment_for_booking_field_request_case import AcceptPaymentForBookingFieldRequestCase
from app.use_case.booking_field_party_request.client.create_client_booking_field_request_case import CreateClientBookingFieldRequestCase
from app.use_case.booking_field_party_request.client.delete_my_booking_field_party_request_case import DeleteMyBookingFieldPartyRequestCase
from app.use_case.booking_field_party_request.client.get_my_booking_field_party_request_case import GetMyBookingFieldPartyRequestCase
from app.use_case.booking_field_party_request.client.paginate_my_booking_field_party_request_case import PaginateMyBookingFieldPartyRequestCase
from app.use_case.booking_field_party_request.client.re_create_client_booking_field_request_by_id_case import ReCreateClientBookingFieldRequestByIdCase
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
            summary="Создать бронирование площадки (Admin)",
            description="Создание нового бронирования площадки (только для администраторов)",
        )(self.create)

        self.router.post(
            "/client/create",
            response_model=CreateBookingFieldPartyResponseDTO,
            summary="Создать бронирование площадки (Client)",
            description="Создание клиентской заявки на бронирование площадки с инициализацией платежа",
        )(self.create_client_booking)

        self.router.post(
            "/client/recreate/{id}",
            response_model=CreateBookingFieldPartyResponseDTO,
            summary="Пересоздать платеж для бронирования (Client)",
            description="Создание новой платежной транзакции для существующей заявки на бронирование",
        )(self.recreate_client_booking)

        self.router.get(
            "/accept-payment",
            response_model=AcceptPaymentForBookingFieldPartyResponseDTO,
            summary="Callback от платежной системы (Common)",
            description="Обработка уведомления от платежной системы Alatau о результате оплаты",
        )(self.accept_payment)

        self.router.get(
            "/client/my",
            response_model=PaginationBookingFieldPartyRequestWithRelationsRDTO,
            summary="Мои бронирования - пагинация (Client)",
            description="Получение пагинированного списка собственных бронирований клиента",
        )(self.paginate_my_bookings)

        self.router.get(
            "/client/my/{id}",
            response_model=BookingFieldPartyRequestWithRelationsRDTO,
            summary="Моё бронирование по ID (Client)",
            description="Получение собственного бронирования по ID с проверкой владельца",
        )(self.get_my_booking)

        self.router.delete(
            "/client/my/delete/{id}",
            response_model=bool,
            summary="Удалить моё бронирование (Client)",
            description="Удаление собственного бронирования (только если статус 'Ожидание оплаты')",
        )(self.delete_my_booking)

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

    async def create_client_booking(
        self,
        dto: CreateBookingFieldPartyRequestDTO,
        current_user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> CreateBookingFieldPartyResponseDTO:
        """
        Создание клиентской заявки на бронирование площадки с инициализацией платежа.

        Args:
            dto: DTO с данными для создания заявки (field_party_id, день, время, контакты)
            current_user: Текущий авторизованный пользователь
            db: Сессия базы данных

        Returns:
            Ответ с созданной заявкой, платежной транзакцией и данными для оплаты
        """
        try:
            return await CreateClientBookingFieldRequestCase(db).execute(dto=dto, user=current_user)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def recreate_client_booking(
        self,
        id: RoutePathConstants.IDPath,
        current_user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> CreateBookingFieldPartyResponseDTO:
        """
        Пересоздание платежной транзакции для существующей заявки на бронирование.

        Используется когда клиент хочет повторить попытку оплаты для существующей заявки.

        Args:
            id: ID существующей заявки на бронирование
            current_user: Текущий авторизованный пользователь (должен быть владельцем заявки)
            db: Сессия базы данных

        Returns:
            Ответ с существующей заявкой и новой платежной транзакцией
        """
        try:
            return await ReCreateClientBookingFieldRequestByIdCase(db).execute(id=id, user=current_user)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def accept_payment(
        self,
        dto: AlatauBackrefGetDTO = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> AcceptPaymentForBookingFieldPartyResponseDTO:
        """
        Обработка callback от платежной системы Alatau.

        Этот эндпоинт вызывается платежной системой после завершения оплаты.
        Не требует авторизации пользователя - безопасность обеспечивается цифровой подписью.

        Args:
            dto: Данные от платежной системы (номер заказа, код результата, подпись)
            db: Сессия базы данных

        Returns:
            Ответ с обновленной заявкой и статусом платежной транзакции
        """
        try:
            return await AcceptPaymentForBookingFieldRequestCase(db).execute(dto=dto)
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

    async def paginate_my_bookings(
        self,
        filter: BookingFieldPartyRequestPaginationFilter = Depends(),
        current_user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationBookingFieldPartyRequestWithRelationsRDTO:
        """
        Получение пагинированного списка собственных бронирований клиента.

        Args:
            filter: Фильтр для пагинации с параметрами сортировки и поиска
            current_user: Текущий авторизованный пользователь
            db: Сессия базы данных

        Returns:
            Пагинированный список собственных бронирований с relationships
        """
        try:
            return await PaginateMyBookingFieldPartyRequestCase(db).execute(filter=filter, user=current_user)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_my_booking(
        self,
        id: RoutePathConstants.IDPath,
        current_user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> BookingFieldPartyRequestWithRelationsRDTO:
        """
        Получение собственного бронирования по ID.

        Проверяет, что бронирование принадлежит текущему пользователю.

        Args:
            id: Уникальный идентификатор бронирования
            current_user: Текущий авторизованный пользователь
            db: Сессия базы данных

        Returns:
            Найденное бронирование с relationships
        """
        try:
            return await GetMyBookingFieldPartyRequestCase(db).execute(id=id, user=current_user)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def delete_my_booking(
        self,
        id: RoutePathConstants.IDPath,
        current_user: UserWithRelationsRDTO = Depends(check_client),
        force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        """
        Удаление собственного бронирования.

        Удаление разрешено только если бронирование имеет статус "Ожидание оплаты" (status_id = 1).

        Args:
            id: Уникальный идентификатор бронирования
            current_user: Текущий авторизованный пользователь
            force_delete: Флаг принудительного удаления
            db: Сессия базы данных

        Returns:
            True если бронирование успешно удалено
        """
        try:
            return await DeleteMyBookingFieldPartyRequestCase(db).execute(id=id, user=current_user, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc