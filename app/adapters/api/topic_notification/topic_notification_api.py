from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.topic_notification.topic_notification_dto import (
    TopicNotificationCDTO,
    TopicNotificationWithRelationsRDTO,
)
from app.adapters.filters.topic_notification.topic_notification_filter import (
    TopicNotificationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.route_constants import RoutePathConstants
from app.use_case.topic_notification.all_topic_notification_case import (
    AllTopicNotificationCase,
)
from app.use_case.topic_notification.create_topic_notification_case import (
    CreateTopicNotificationCase,
)
from app.use_case.topic_notification.delete_topic_notification_case import (
    DeleteTopicNotificationByIdCase,
)
from app.use_case.topic_notification.get_topic_notification_by_id_case import (
    GetTopicNotificationByIdCase,
)
from app.use_case.topic_notification.update_topic_notification_case import (
    UpdateTopicNotificationCase,
)
from app.use_case.topic_notification.update_topic_notification_image_case import (
    UpdateTopicNotificationImageCase,
)


class TopicNotificationApi:
    def __init__(self) -> None:
        """
        Инициализация TopicNotificationApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API топиков уведомлений.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=list[TopicNotificationWithRelationsRDTO],
            summary="Список топиков уведомлений",
            description="Получение списка всех топиков уведомлений",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=TopicNotificationWithRelationsRDTO,
            summary="Создать топик уведомления",
            description="Создание нового топика уведомления",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=TopicNotificationWithRelationsRDTO,
            summary="Обновить топик уведомления по ID",
            description="Обновление топика уведомления по ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=TopicNotificationWithRelationsRDTO,
            summary="Получить топик уведомления по ID",
            description="Получение топика уведомления по ID",
        )(self.get_by_id)

        self.router.put(
            "/update-image/{id}",
            response_model=TopicNotificationWithRelationsRDTO,
            summary="Обновить изображение топика",
            description="Обновление изображения топика уведомления по его ID",
        )(self.update_image)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить топик уведомления по ID",
            description="Удаление топика уведомления по ID",
        )(self.delete)

    async def get_all(
        self,
        filter: TopicNotificationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[TopicNotificationWithRelationsRDTO]:
        try:
            return await AllTopicNotificationCase(db).execute(filter)
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
        dto: TopicNotificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> TopicNotificationWithRelationsRDTO:
        try:
            return await CreateTopicNotificationCase(db).execute(dto=dto)
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
        dto: TopicNotificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> TopicNotificationWithRelationsRDTO:
        try:
            return await UpdateTopicNotificationCase(db).execute(id=id, dto=dto)
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
    ) -> TopicNotificationWithRelationsRDTO:
        try:
            return await GetTopicNotificationByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def update_image(
        self,
        id: RoutePathConstants.IDPath,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
    ) -> TopicNotificationWithRelationsRDTO:
        try:
            return await UpdateTopicNotificationImageCase(db).execute(id=id, file=file)
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
            return await DeleteTopicNotificationByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc
