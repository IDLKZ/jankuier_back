from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.notification.notification_dto import (
    NotificationCDTO,
    NotificationWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import PaginationNotificationWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.filters.notification.notification_pagination_filter import (
    NotificationPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_current_user
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.route_constants import RoutePathConstants
from app.use_case.notification.create_notification_case import CreateNotificationCase
from app.use_case.notification.delete_notification_case import (
    DeleteNotificationByIdCase,
)
from app.use_case.notification.get_notification_by_id_case import (
    GetNotificationByIdCase,
)
from app.use_case.notification.paginate_notification_case import (
    PaginateNotificationCase,
)
from app.use_case.notification.update_notification_case import UpdateNotificationCase
from app.use_case.notification.client.get_client_notification_by_id_case import (
    GetClientNotificationByIdCase,
)
from app.use_case.notification.client.paginate_client_notification_case import (
    PaginateClientNotificationCase,
)


class NotificationApi:
    def __init__(self) -> None:
        """
        Инициализация NotificationApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API уведомлений.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationNotificationWithRelationsRDTO,
            summary="Список уведомлений с пагинацией",
            description="Получение списка уведомлений с постраничной фильтрацией",
        )(self.paginate)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=NotificationWithRelationsRDTO,
            summary="Создать уведомление",
            description="Создание нового уведомления",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=NotificationWithRelationsRDTO,
            summary="Обновить уведомление по ID",
            description="Обновление уведомления по ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=NotificationWithRelationsRDTO,
            summary="Получить уведомление по ID",
            description="Получение информации об уведомлении по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить уведомление по ID",
            description="Удаление уведомления по ID",
        )(self.delete)

        # Client routes
        self.router.get(
            "/client",
            response_model=PaginationNotificationWithRelationsRDTO,
            summary="Список уведомлений клиента с пагинацией",
            description="Получение списка уведомлений текущего клиента с постраничной фильтрацией",
        )(self.paginate_client)

        self.router.get(
            "/client/get/{id}",
            response_model=NotificationWithRelationsRDTO,
            summary="Получить уведомление клиента по ID",
            description="Получение уведомления текущего клиента по ID с автоматической отметкой о прочтении",
        )(self.get_client_by_id)

    async def paginate(
        self,
        filter: NotificationPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationNotificationWithRelationsRDTO:
        try:
            return await PaginateNotificationCase(db).execute(filter)
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
        dto: NotificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> NotificationWithRelationsRDTO:
        try:
            return await CreateNotificationCase(db).execute(dto=dto)
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
        dto: NotificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> NotificationWithRelationsRDTO:
        try:
            return await UpdateNotificationCase(db).execute(id=id, dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_by_id(
        self,
        id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> NotificationWithRelationsRDTO:
        try:
            return await GetNotificationByIdCase(db).execute(id=id)
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
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        try:
            return await DeleteNotificationByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def paginate_client(
        self,
        filter: NotificationPaginationFilter = Depends(),
        current_user: UserWithRelationsRDTO = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationNotificationWithRelationsRDTO:
        """
        Получение пагинированного списка уведомлений текущего клиента.
        Показывает личные уведомления и общие уведомления по топикам.
        """
        try:
            return await PaginateClientNotificationCase(db).execute(
                filter=filter, user=current_user
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_client_by_id(
        self,
        id: RoutePathConstants.IDPath,
        current_user: UserWithRelationsRDTO = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> NotificationWithRelationsRDTO:
        """
        Получение уведомления клиента по ID с автоматической отметкой о прочтении.
        """
        try:
            return await GetClientNotificationByIdCase(db).execute(
                id=id, user=current_user
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc
