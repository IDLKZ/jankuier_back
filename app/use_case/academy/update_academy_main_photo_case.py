from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy.academy_dto import (
    AcademyWithRelationsRDTO,
    AcademyUpdateDTO,
)
from app.adapters.repository.academy.academy_repository import AcademyRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class UpdateAcademyMainPhotoCase(BaseUseCase[AcademyWithRelationsRDTO]):
    """
    Класс Use Case для обновления главного изображения академии.

    Использует:
        - Репозиторий `AcademyRepository` для работы с базой данных.
        - `FileService` для работы с изображениями.

    Атрибуты:
        repository (AcademyRepository): Репозиторий для работы с академиями.
        file_service (FileService): Сервис для работы с файлами.
        model (AcademyEntity | None): Модель академии для обновления.

    Методы:
        execute(id: int, file: UploadFile) -> AcademyWithRelationsRDTO:
            Выполняет обновление главного изображения академии.
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
        self.repository = AcademyRepository(db)
        self.file_service = FileService(db)
        self.model: AcademyEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(self, id: int, file: UploadFile) -> AcademyWithRelationsRDTO:
        """
        Выполняет операцию обновления главного изображения академии.

        Args:
            id (int): Идентификатор академии.
            file (UploadFile): Файл изображения академии.

        Returns:
            AcademyWithRelationsRDTO: Обновленный объект академии с отношениями.

        Raises:
            AppExceptionResponse: Если академия не найдена или файл не валиден.
        """
        await self.validate(id=id, file=file)
        dto = await self.transform(file=file)

        # Обновляем академию используя repository.update
        self.model = await self.repository.update(obj=self.model, dto=dto)

        # Получаем обновленную академию с отношениями
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return AcademyWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, file: UploadFile) -> None:
        """
        Валидирует данные перед обновлением главного изображения академии.

        Args:
            id (int): Идентификатор академии.
            file (UploadFile): Файл изображения для валидации.

        Raises:
            AppExceptionResponse: Если академия не найдена или файл не валиден.
        """
        # Проверка существования академии
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))

        # Валидация файла изображения
        if not file:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("file_is_required")
            )

        self.file_service.validate_file(file, self.extensions)

    async def transform(self, file: UploadFile) -> AcademyUpdateDTO:
        """
        Трансформирует данные перед обновлением главного изображения академии.

        Args:
            file (UploadFile): Файл изображения для обновления.

        Returns:
            AcademyUpdateDTO: DTO с обновленным image_id.
        """
        # Определение папки для загрузки изображений академий
        self.upload_folder = f"academies/images/{self.model.value}"

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
        return AcademyUpdateDTO(image_id=file_entity.id)