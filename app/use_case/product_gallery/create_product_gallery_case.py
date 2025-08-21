from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_gallery.product_gallery_dto import (
    ProductGalleryCDTO,
    ProductGalleryWithRelationsRDTO,
)
from app.adapters.repository.file.file_repository import FileRepository
from app.adapters.repository.product.product_repository import ProductRepository
from app.adapters.repository.product_gallery.product_gallery_repository import (
    ProductGalleryRepository,
)
from app.adapters.repository.product_variant.product_variant_repository import (
    ProductVariantRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductGalleryEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class CreateProductGalleryCase(BaseUseCase[ProductGalleryWithRelationsRDTO]):
    """
    Класс Use Case для создания нового изображения в галерее товара.

    Использует:
        - Репозиторий `ProductGalleryRepository` для работы с базой данных.
        - DTO `ProductGalleryCDTO` для входных данных.
        - DTO `ProductGalleryWithRelationsRDTO` для возврата данных с отношениями.
        - `FileService` для работы с изображениями.

    Атрибуты:
        repository (ProductGalleryRepository): Репозиторий для работы с изображениями галереи товаров.
        product_repository (ProductRepository): Репозиторий для работы с товарами.
        product_variant_repository (ProductVariantRepository): Репозиторий для работы с вариантами товаров.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (ProductGalleryEntity | None): Модель изображения галереи товара для создания.

    Методы:
        execute(dto: ProductGalleryCDTO, file: UploadFile | None = None) -> ProductGalleryWithRelationsRDTO:
            Выполняет создание изображения в галерее товара.
        validate(dto: ProductGalleryCDTO, file: UploadFile | None = None):
            Валидирует данные перед созданием.
        transform(dto: ProductGalleryCDTO, file: UploadFile | None = None):
            Трансформирует данные перед созданием.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductGalleryRepository(db)
        self.product_repository = ProductRepository(db)
        self.product_variant_repository = ProductVariantRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: ProductGalleryEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, dto: ProductGalleryCDTO, file: UploadFile | None = None
    ) -> ProductGalleryWithRelationsRDTO:
        """
        Выполняет операцию создания нового изображения в галерее товара.

        Args:
            dto (ProductGalleryCDTO): DTO с данными для создания изображения галереи товара.
            file (UploadFile | None): Опциональный файл изображения для загрузки.

        Returns:
            ProductGalleryWithRelationsRDTO: Созданный объект изображения галереи товара с отношениями.

        Raises:
            AppExceptionResponse: Если связанные сущности не найдены или валидация не прошла.
        """
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        self.model = await self.repository.create(obj=self.model)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return ProductGalleryWithRelationsRDTO.from_orm(self.model)

    async def validate(
        self, dto: ProductGalleryCDTO, file: UploadFile | None = None
    ) -> None:
        """
        Валидирует данные перед созданием изображения галереи товара.

        Args:
            dto (ProductGalleryCDTO): DTO с данными для валидации.
            file (UploadFile | None): Опциональный файл изображения для валидации.

        Raises:
            AppExceptionResponse: Если связанные сущности не найдены или файл не валиден.
        """
        # Проверка существования товара
        product = await self.product_repository.get(dto.product_id)
        if not product:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_not_found_by_id")
            )

        # Проверка существования варианта товара (если указан)
        if dto.variant_id is not None:
            variant = await self.product_variant_repository.get(dto.variant_id)
            if not variant:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("product_variant_not_found_by_id")
                )

            # Проверка что вариант принадлежит указанному товару
            if variant.product_id != dto.product_id:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("product_variant_does_not_belong_to_product")
                )

        # Проверка существования файла по file_id (если указан)
        if dto.file_id is not None:
            if (await self.file_repository.get(dto.file_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("file_not_found_by_id")
                )

        # Валидация файла изображения (если предоставлен)
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка что указан либо file_id, либо file для загрузки
        if dto.file_id is None and file is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("either_file_id_or_file_required")
            )

    async def transform(self, dto: ProductGalleryCDTO, file: UploadFile | None = None):
        """
        Трансформирует данные перед созданием изображения галереи товара.

        Args:
            dto (ProductGalleryCDTO): DTO с данными для трансформации.
            file (UploadFile | None): Опциональный файл изображения для сохранения.
        """
        # Получение значения товара для папки загрузки
        product = await self.product_repository.get(dto.product_id)
        self.upload_folder = AppFileExtensionConstants.product_image_directory(
            product.value
        )

        # Сохранение файла если предоставлен
        if file:
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.file_id = file_entity.id

        # Создание модели для сохранения
        self.model = ProductGalleryEntity(**dto.dict())
