from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product.product_dto import ProductWithRelationsRDTO, ProductUpdateDTO
from app.adapters.repository.product.product_repository import ProductRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class UpdateProductMainPhotoCase(BaseUseCase[ProductWithRelationsRDTO]):
    """
    Класс Use Case для обновления главного изображения товара.

    Использует:
        - Репозиторий `ProductRepository` для работы с базой данных.
        - `FileService` для работы с изображениями.

    Атрибуты:
        repository (ProductRepository): Репозиторий для работы с товарами.
        file_service (FileService): Сервис для работы с файлами.
        model (ProductEntity | None): Модель товара для обновления.

    Методы:
        execute(id: int, file: UploadFile) -> ProductWithRelationsRDTO:
            Выполняет обновление главного изображения товара.
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
        self.repository = ProductRepository(db)
        self.file_service = FileService(db)
        self.model: ProductEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(self, id: int, file: UploadFile) -> ProductWithRelationsRDTO:
        """
        Выполняет операцию обновления главного изображения товара.

        Args:
            id (int): Идентификатор товара.
            file (UploadFile): Файл изображения товара.

        Returns:
            ProductWithRelationsRDTO: Обновленный объект товара с отношениями.

        Raises:
            AppExceptionResponse: Если товар не найден или файл не валиден.
        """
        await self.validate(id=id, file=file)
        dto = await self.transform(file=file)

        # Обновляем товар используя repository.update
        self.model = await self.repository.update(obj=self.model, dto=dto)

        # Получаем обновленный товар с отношениями
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return ProductWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, file: UploadFile) -> None:
        """
        Валидирует данные перед обновлением главного изображения товара.

        Args:
            id (int): Идентификатор товара.
            file (UploadFile): Файл изображения для валидации.

        Raises:
            AppExceptionResponse: Если товар не найден или файл не валиден.
        """
        # Проверка существования товара
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))

        # Валидация файла изображения
        if not file:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("file_is_required")
            )

        self.file_service.validate_file(file, self.extensions)

    async def transform(self, file: UploadFile) -> ProductUpdateDTO:
        """
        Трансформирует данные перед обновлением главного изображения товара.

        Args:
            file (UploadFile): Файл изображения для обновления.

        Returns:
            ProductUpdateDTO: DTO с обновленным image_id.
        """
        # Определение папки для загрузки изображений товаров
        self.upload_folder = AppFileExtensionConstants.product_image_directory(
            self.model.value
        )

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
        return ProductUpdateDTO(image_id=file_entity.id)