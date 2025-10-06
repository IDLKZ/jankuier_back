from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.topic_notification.topic_notification_dto import (
    TopicNotificationCDTO,
    TopicNotificationWithRelationsRDTO,
)
from app.adapters.repository.topic_notification.topic_notification_repository import (
    TopicNotificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TopicNotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class UpdateTopicNotificationImageCase(BaseUseCase[TopicNotificationWithRelationsRDTO]):
    """
    Use Case для обновления изображения топика уведомления.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TopicNotificationRepository(db)
        self.file_service = FileService(db)
        self.model: TopicNotificationEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, id: int, file: UploadFile
    ) -> TopicNotificationWithRelationsRDTO:
        await self.validate(id=id, file=file)
        dto = await self.transform(file=file)

        self.model = await self.repository.update(obj=self.model, dto=dto)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return TopicNotificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, file: UploadFile) -> None:
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))

        if not file:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("file_is_required")
            )

        self.file_service.validate_file(file, self.extensions)

    async def transform(self, file: UploadFile) -> TopicNotificationCDTO:
        self.upload_folder = f"topic_notifications/images/{self.model.value}"

        if self.model.image_id is not None:
            file_entity = await self.file_service.update_file(
                file_id=self.model.image_id,
                new_file=file,
                uploaded_folder=self.upload_folder,
                extensions=self.extensions,
            )
        else:
            file_entity = await self.file_service.save_file(
                file=file,
                uploaded_folder=self.upload_folder,
                extensions=self.extensions,
            )

        return TopicNotificationCDTO(
            image_id=file_entity.id,
            title_ru=self.model.title_ru,
            title_kk=self.model.title_kk,
            title_en=self.model.title_en,
            value=self.model.value,
        )
