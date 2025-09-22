from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party.field_party_dto import (
    FieldPartyWithRelationsRDTO,
    FieldPartyUpdateDTO,
)
from app.adapters.repository.field_party.field_party_repository import (
    FieldPartyRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldPartyEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class UpdateFieldPartyMainPhotoCase(BaseUseCase[FieldPartyWithRelationsRDTO]):
    """
    Класс Use Case для обновления главного изображения площадки поля.

    Использует:
        - Репозиторий `FieldPartyRepository` для работы с базой данных.
        - `FileService` для работы с изображениями.

    Атрибуты:
        repository (FieldPartyRepository): Репозиторий для работы с площадками полей.
        file_service (FileService): Сервис для работы с файлами.
        model (FieldPartyEntity | None): Модель площадки поля для обновления.

    Методы:
        execute(id: int, file: UploadFile) -> FieldPartyWithRelationsRDTO:
            Выполняет обновление главного изображения площадки поля.
        validate(id: int, file: UploadFile):
            Валидирует данные перед обновлением.
        transform(file: UploadFile):
            Трансформирует данные перед обновлением.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyRepository(db)
        self.file_service = FileService(db)
        self.model: FieldPartyEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(self, id: int, file: UploadFile) -> FieldPartyWithRelationsRDTO:
        """
        Выполняет операцию обновления главного изображения площадки поля.

        Args:
            id (int): Идентификатор площадки поля.
            file (UploadFile): Файл изображения площадки поля.

        Returns:
            FieldPartyWithRelationsRDTO: Обновленный объект площадки поля с отношениями.

        Raises:
            AppExceptionResponse: Если площадка поля не найдена или файл не валиден.
        """
        await self.validate(id=id, file=file)
        dto = await self.transform(file=file)

        # Обновляем площадку поля используя repository.update
        self.model = await self.repository.update(obj=self.model, dto=dto)

        # Получаем обновленную площадку поля с отношениями
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return FieldPartyWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, file: UploadFile) -> None:
        """
        Валидирует данные перед обновлением главного изображения площадки поля.

        Args:
            id (int): Идентификатор площадки поля.
            file (UploadFile): Файл изображения для валидации.

        Raises:
            AppExceptionResponse: Если площадка поля не найдена или файл не валиден.
        """
        # Проверка существования площадки поля
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Валидация файла изображения
        if not file:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("file_is_required")
            )

        self.file_service.validate_file(file, self.extensions)

    async def transform(self, file: UploadFile) -> FieldPartyUpdateDTO:
        """
        Трансформирует данные перед обновлением главного изображения площадки поля.

        Args:
            file (UploadFile): Файл изображения для обновления.

        Returns:
            FieldPartyUpdateDTO: DTO с обновленным image_id.
        """
        # Определение папки для загрузки изображений площадок полей
        self.upload_folder = f"field_parties/images/{self.model.value}"

        # Обработка файла изображения
        if self.model.image_id is not None:
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

        # Создаем DTO только с обновленным image_id
        return FieldPartyUpdateDTO(image_id=file_entity.id)