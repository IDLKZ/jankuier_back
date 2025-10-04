from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.firebase_notification.firebase_notification_dto import (
    FirebaseNotificationCDTO,
    FirebaseNotificationWithRelationsRDTO,
    FirebaseNotificationClientCDTO,
)
from app.adapters.dto.pagination_dto import (
    PaginationFirebaseNotificationWithRelationsRDTO,
)
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.filters.firebase_notification.firebase_notification_pagination_filter import (
    FirebaseNotificationPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_current_user
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.route_constants import RoutePathConstants
from app.use_case.firebase_notification.create_firebase_notification_case import (
    CreateFirebaseNotificationCase,
)
from app.use_case.firebase_notification.delete_firebase_notification_case import (
    DeleteFirebaseNotificationByIdCase,
)
from app.use_case.firebase_notification.get_firebase_notification_by_id_case import (
    GetFirebaseNotificationByIdCase,
)
from app.use_case.firebase_notification.paginate_firebase_notification_case import (
    PaginateFirebaseNotificationCase,
)
from app.use_case.firebase_notification.update_firebase_notification_case import (
    UpdateFirebaseNotificationCase,
)
from app.use_case.firebase_notification.client.create_or_update_client_firebase_notification_case import (
    CreateOrUpdateClientFirebaseNotificationCase,
)
from app.use_case.firebase_notification.client.get_client_firebase_notification_by_id_case import (
    GetClientFirebaseNotificationByIdCase,
)


class FirebaseNotificationApi:
    def __init__(self) -> None:
        """
        Инициализация FirebaseNotificationApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API Firebase уведомлений.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationFirebaseNotificationWithRelationsRDTO,
            summary="Список Firebase уведомлений с пагинацией",
            description="Получение списка Firebase токенов с постраничной фильтрацией",
        )(self.paginate)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=FirebaseNotificationWithRelationsRDTO,
            summary="Создать Firebase токен",
            description="Создание нового Firebase токена для уведомлений",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=FirebaseNotificationWithRelationsRDTO,
            summary="Обновить Firebase токен по ID",
            description="Обновление Firebase токена по ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=FirebaseNotificationWithRelationsRDTO,
            summary="Получить Firebase токен по ID",
            description="Получение информации о Firebase токене по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить Firebase токен по ID",
            description="Удаление Firebase токена по ID",
        )(self.delete)

        # Client routes
        self.router.get(
            "/client/get",
            response_model=FirebaseNotificationWithRelationsRDTO | None,
            summary="Получить Firebase токен клиента",
            description="Получение Firebase токена текущего клиента",
        )(self.get_client_firebase_notification)

        self.router.post(
            "/client/create-or-update",
            response_model=FirebaseNotificationWithRelationsRDTO,
            summary="Создать или обновить Firebase токен клиента",
            description="Создание или обновление Firebase токена текущего клиента",
        )(self.create_or_update_client_firebase_notification)

    async def paginate(
        self,
        filter: FirebaseNotificationPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationFirebaseNotificationWithRelationsRDTO:
        try:
            return await PaginateFirebaseNotificationCase(db).execute(filter)
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
        dto: FirebaseNotificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> FirebaseNotificationWithRelationsRDTO:
        try:
            return await CreateFirebaseNotificationCase(db).execute(dto=dto)
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
        dto: FirebaseNotificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> FirebaseNotificationWithRelationsRDTO:
        try:
            return await UpdateFirebaseNotificationCase(db).execute(id=id, dto=dto)
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
    ) -> FirebaseNotificationWithRelationsRDTO:
        try:
            return await GetFirebaseNotificationByIdCase(db).execute(id=id)
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
            return await DeleteFirebaseNotificationByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_client_firebase_notification(
        self,
        current_user: UserWithRelationsRDTO = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> FirebaseNotificationWithRelationsRDTO | None:
        """
        Получение Firebase токена текущего клиента.
        """
        try:
            return await GetClientFirebaseNotificationByIdCase(db).execute(
                 user=current_user
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def create_or_update_client_firebase_notification(
        self,
        dto: FirebaseNotificationClientCDTO,
        current_user: UserWithRelationsRDTO = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> FirebaseNotificationWithRelationsRDTO:
        """
        Создание или обновление Firebase токена текущего клиента.
        """
        try:
            return await CreateOrUpdateClientFirebaseNotificationCase(db).execute(
                dto=dto, user=current_user
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc
