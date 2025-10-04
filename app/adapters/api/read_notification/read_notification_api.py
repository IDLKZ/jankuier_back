from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationReadNotificationWithRelationsRDTO
from app.adapters.dto.read_notification.read_notification_dto import (
    ReadNotificationCDTO,
    ReadNotificationWithRelationsRDTO,
)
from app.adapters.dto.topic_notification.topic_notification_dto import (
    TopicNotificationWithRelationsRDTO,
)
from app.adapters.filters.read_notification.read_notification_pagination_filter import (
    ReadNotificationPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.route_constants import RoutePathConstants
from app.use_case.read_notification.create_read_notification_case import (
    CreateReadNotificationCase,
)
from app.use_case.read_notification.delete_read_notification_case import (
    DeleteReadNotificationByIdCase,
)
from app.use_case.read_notification.get_read_notification_by_id_case import (
    GetReadNotificationByIdCase,
)
from app.use_case.read_notification.get_topics_by_user_id_case import (
    GetTopicsByUserIdCase,
)
from app.use_case.read_notification.paginate_read_notification_case import (
    PaginateReadNotificationCase,
)
from app.use_case.read_notification.update_read_notification_case import (
    UpdateReadNotificationCase,
)


class ReadNotificationApi:
    def __init__(self) -> None:
        """
        Инициализация ReadNotificationApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API прочитанных уведомлений.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationReadNotificationWithRelationsRDTO,
            summary="Список прочитанных уведомлений с пагинацией",
            description="Получение списка прочитанных уведомлений с постраничной фильтрацией",
        )(self.paginate)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=ReadNotificationWithRelationsRDTO,
            summary="Отметить уведомление как прочитанное",
            description="Создание записи о прочитанном уведомлении",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=ReadNotificationWithRelationsRDTO,
            summary="Обновить запись о прочитанном уведомлении по ID",
            description="Обновление записи о прочитанном уведомлении по ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=ReadNotificationWithRelationsRDTO,
            summary="Получить запись о прочитанном уведомлении по ID",
            description="Получение информации о прочитанном уведомлении по ID",
        )(self.get_by_id)

        self.router.get(
            "/topics/{user_id}",
            response_model=list[TopicNotificationWithRelationsRDTO],
            summary="Получить топики уведомлений прочитанных пользователем",
            description="Получение уникальных топиков уведомлений, которые прочитал пользователь",
        )(self.get_topics_by_user_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить запись о прочитанном уведомлении по ID",
            description="Удаление записи о прочитанном уведомлении по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: ReadNotificationPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationReadNotificationWithRelationsRDTO:
        try:
            return await PaginateReadNotificationCase(db).execute(filter)
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
        dto: ReadNotificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ReadNotificationWithRelationsRDTO:
        try:
            return await CreateReadNotificationCase(db).execute(dto=dto)
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
        dto: ReadNotificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ReadNotificationWithRelationsRDTO:
        try:
            return await UpdateReadNotificationCase(db).execute(id=id, dto=dto)
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
    ) -> ReadNotificationWithRelationsRDTO:
        try:
            return await GetReadNotificationByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_topics_by_user_id(
        self,
        user_id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> list[TopicNotificationWithRelationsRDTO]:
        try:
            return await GetTopicsByUserIdCase(db).execute(user_id=user_id)
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
            return await DeleteReadNotificationByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc
