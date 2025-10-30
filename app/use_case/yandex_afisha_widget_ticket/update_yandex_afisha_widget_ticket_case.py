from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_dto import (
    YandexAfishaWidgetTicketCDTO,
    YandexAfishaWidgetTicketWithRelationsRDTO,
)
from app.adapters.repository.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_repository import (
    YandexAfishaWidgetTicketRepository,
)
from app.adapters.repository.file.file_repository import FileRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import YandexAfishaWidgetTicketEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class UpdateYandexAfishaWidgetTicketCase(
    BaseUseCase[YandexAfishaWidgetTicketWithRelationsRDTO]
):
    """
    Класс Use Case для обновления билета Яндекс.Афиша.

    Использует:
        - Репозиторий `YandexAfishaWidgetTicketRepository` для работы с базой данных.
        - Репозиторий `FileRepository` для проверки существования файла.
        - Сервис `FileService` для работы с файлами.
        - DTO `YandexAfishaWidgetTicketCDTO` для входных данных.
        - DTO `YandexAfishaWidgetTicketWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (YandexAfishaWidgetTicketRepository): Репозиторий для работы с билетами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (YandexAfishaWidgetTicketEntity | None): Обновляемая модель билета.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = YandexAfishaWidgetTicketRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: YandexAfishaWidgetTicketEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self,
        id: int,
        dto: YandexAfishaWidgetTicketCDTO,
        file: UploadFile | None = None,
    ) -> YandexAfishaWidgetTicketWithRelationsRDTO:
        """
        Выполняет операцию обновления билета Яндекс.Афиша.

        Args:
            id (int): Идентификатор билета.
            dto (YandexAfishaWidgetTicketCDTO): Данные для обновления билета.
            file (UploadFile | None): Файл изображения билета.

        Returns:
            YandexAfishaWidgetTicketWithRelationsRDTO: Обновленный билет с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto, file=file)
        await self.transform(id=id, dto=dto, file=file)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return YandexAfishaWidgetTicketWithRelationsRDTO.from_orm(model)

    async def validate(
        self, id: int, dto: YandexAfishaWidgetTicketCDTO, file: UploadFile | None = None
    ) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор билета для проверки.
            dto (YandexAfishaWidgetTicketCDTO): Данные для валидации.
            file (UploadFile | None): Файл для валидации.

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
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла изображения по ID
        if dto.image_id and self.model.image_id != dto.image_id:
            image = await self.file_repository.get(dto.image_id)
            if not image:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("image_not_found_by_id")
                )

    async def transform(
        self, id: int, dto: YandexAfishaWidgetTicketCDTO, file: UploadFile | None = None
    ) -> None:
        """
        Преобразование входных данных.

        Args:
            id (int): Идентификатор билета.
            dto (YandexAfishaWidgetTicketCDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        # Обработка файла
        if file:
            self.upload_folder = (
                AppFileExtensionConstants.yandex_afisha_widget_ticket_image_directory(
                    dto.yandex_session_id
                )
            )
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
            dto.image_id = file_entity.id
