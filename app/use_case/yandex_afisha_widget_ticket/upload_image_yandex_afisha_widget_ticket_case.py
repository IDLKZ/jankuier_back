from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_dto import (
    YandexAfishaWidgetTicketWithRelationsRDTO,
)
from app.adapters.repository.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_repository import (
    YandexAfishaWidgetTicketRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import YandexAfishaWidgetTicketEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class ImageUpdateDTO(BaseModel):
    """DTO для обновления только image_id"""

    image_id: int | None = None

    class Config:
        from_attributes = True


class UploadImageYandexAfishaWidgetTicketCase(
    BaseUseCase[YandexAfishaWidgetTicketWithRelationsRDTO]
):
    """
    Класс Use Case для загрузки/обновления изображения билета Яндекс.Афиша.

    Использует:
        - Репозиторий `YandexAfishaWidgetTicketRepository` для работы с базой данных.
        - Сервис `FileService` для работы с файлами.
        - DTO `YandexAfishaWidgetTicketWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (YandexAfishaWidgetTicketRepository): Репозиторий для работы с билетами.
        file_service (FileService): Сервис для работы с файлами.
        model (YandexAfishaWidgetTicketEntity | None): Модель билета.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = YandexAfishaWidgetTicketRepository(db)
        self.file_service = FileService(db)
        self.model: YandexAfishaWidgetTicketEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, id: int, file: UploadFile
    ) -> YandexAfishaWidgetTicketWithRelationsRDTO:
        """
        Выполняет операцию загрузки/обновления изображения билета.

        Args:
            id (int): Идентификатор билета.
            file (UploadFile): Файл изображения.

        Returns:
            YandexAfishaWidgetTicketWithRelationsRDTO: Билет с обновленным изображением.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, file=file)
        await self.transform(id=id, file=file)

        # Обновляем модель в БД
        self.model = await self.repository.get(id)
        model = await self.repository.get(
            id, options=self.repository.default_relationships()
        )
        return YandexAfishaWidgetTicketWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int, file: UploadFile) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор билета для проверки.
            file (UploadFile): Файл для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования билета
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("yandex_afisha_widget_ticket_not_found")
            )

        # Проверка файла изображения
        if not file:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("file_is_required")
            )

        self.file_service.validate_file(file, self.extensions)

    async def transform(self, id: int, file: UploadFile) -> None:
        """
        Преобразование и сохранение файла.

        Args:
            id (int): Идентификатор билета.
            file (UploadFile): Файл для сохранения.
        """
        # Генерация пути для загрузки
        self.upload_folder = (
            AppFileExtensionConstants.yandex_afisha_widget_ticket_image_directory(
                self.model.yandex_session_id
            )
        )

        # Обновление или создание файла
        if self.model.image_id:
            # Обновление существующего файла
            file_entity = await self.file_service.update_file(
                file_id=self.model.image_id,
                new_file=file,
                uploaded_folder=self.upload_folder,
                extensions=self.extensions,
            )
        else:
            # Создание нового файла
            file_entity = await self.file_service.save_file(
                file=file,
                uploaded_folder=self.upload_folder,
                extensions=self.extensions,
            )

        # Обновление image_id в модели
        self.model.image_id = file_entity.id
        image_dto = ImageUpdateDTO(image_id=file_entity.id)
        await self.repository.update(obj=self.model, dto=image_dto)
