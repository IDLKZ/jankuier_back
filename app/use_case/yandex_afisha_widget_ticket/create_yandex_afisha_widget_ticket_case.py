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


class CreateYandexAfishaWidgetTicketCase(
    BaseUseCase[YandexAfishaWidgetTicketWithRelationsRDTO]
):
    """
    Класс Use Case для создания нового билета Яндекс.Афиша.

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
        model (YandexAfishaWidgetTicketEntity | None): Созданная модель билета.
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
        self, dto: YandexAfishaWidgetTicketCDTO, file: UploadFile | None = None
    ) -> YandexAfishaWidgetTicketWithRelationsRDTO:
        """
        Выполняет операцию создания билета Яндекс.Афиша.

        Args:
            dto (YandexAfishaWidgetTicketCDTO): Данные для создания билета.
            file (UploadFile | None): Файл изображения билета.

        Returns:
            YandexAfishaWidgetTicketWithRelationsRDTO: Созданный билет с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return YandexAfishaWidgetTicketWithRelationsRDTO.from_orm(model)

    async def validate(
        self, dto: YandexAfishaWidgetTicketCDTO, file: UploadFile | None = None
    ) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (YandexAfishaWidgetTicketCDTO): Данные для валидации.
            file (UploadFile | None): Файл для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка файла изображения
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла изображения по ID
        if dto.image_id:
            image = await self.file_repository.get(dto.image_id)
            if not image:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("image_not_found_by_id")
                )

    async def transform(
        self, dto: YandexAfishaWidgetTicketCDTO, file: UploadFile | None = None
    ) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (YandexAfishaWidgetTicketCDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        # Сохранение файла
        if file:
            self.upload_folder = (
                AppFileExtensionConstants.yandex_afisha_widget_ticket_image_directory(
                    dto.yandex_session_id
                )
            )
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.image_id = file_entity.id

        self.model = YandexAfishaWidgetTicketEntity(**dto.dict())
