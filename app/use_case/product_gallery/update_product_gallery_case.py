from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_gallery.product_gallery_dto import ProductGalleryUpdateDTO, ProductGalleryWithRelationsRDTO
from app.adapters.repository.file.file_repository import FileRepository
from app.adapters.repository.product.product_repository import ProductRepository
from app.adapters.repository.product_gallery.product_gallery_repository import ProductGalleryRepository
from app.adapters.repository.product_variant.product_variant_repository import ProductVariantRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductGalleryEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class UpdateProductGalleryCase(BaseUseCase[ProductGalleryWithRelationsRDTO]):
    """
    Класс Use Case для обновления изображения в галерее товара.

    Использует:
        - Репозиторий `ProductGalleryRepository` для работы с базой данных.
        - DTO `ProductGalleryUpdateDTO` для входных данных.
        - DTO `ProductGalleryWithRelationsRDTO` для возврата данных с отношениями.
        - `FileService` для работы с изображениями.

    Атрибуты:
        repository (ProductGalleryRepository): Репозиторий для работы с изображениями галереи товаров.
        product_repository (ProductRepository): Репозиторий для работы с товарами.
        product_variant_repository (ProductVariantRepository): Репозиторий для работы с вариантами товаров.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (ProductGalleryEntity | None): Модель изображения галереи товара для обновления.

    Методы:
        execute(id: int, dto: ProductGalleryUpdateDTO, file: UploadFile | None = None) -> ProductGalleryWithRelationsRDTO:
            Выполняет обновление изображения в галерее товара.
        validate(id: int, dto: ProductGalleryUpdateDTO, file: UploadFile | None = None):
            Валидирует данные перед обновлением.
        transform(dto: ProductGalleryUpdateDTO, file: UploadFile | None = None):
            Трансформирует данные перед обновлением.
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
        self, id: int, dto: ProductGalleryUpdateDTO, file: UploadFile | None = None
    ) -> ProductGalleryWithRelationsRDTO:
        """
        Выполняет операцию обновления изображения в галерее товара.

        Args:
            id (int): Идентификатор изображения галереи товара для обновления.
            dto (ProductGalleryUpdateDTO): DTO с данными для обновления изображения галереи товара.
            file (UploadFile | None): Опциональный файл изображения для замены.

        Returns:
            ProductGalleryWithRelationsRDTO: Обновленный объект изображения галереи товара с отношениями.

        Raises:
            AppExceptionResponse: Если изображение не найдено, связанные сущности не найдены или валидация не прошла.
        """
        await self.validate(id=id, dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        self.model = await self.repository.update(obj=self.model, dto=dto)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return ProductGalleryWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, dto: ProductGalleryUpdateDTO, file: UploadFile | None = None) -> None:
        """
        Валидирует данные перед обновлением изображения галереи товара.

        Args:
            id (int): Идентификатор изображения галереи товара для обновления.
            dto (ProductGalleryUpdateDTO): DTO с данными для валидации.
            file (UploadFile | None): Опциональный файл изображения для валидации.

        Raises:
            AppExceptionResponse: Если изображение не найдено, связанные сущности не найдены или файл не валиден.
        """
        # Проверка существования изображения галереи товара
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Проверка существования варианта товара (если указан новый)
        if dto.variant_id is not None:
            variant = await self.product_variant_repository.get(dto.variant_id)
            if not variant:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("product_variant_not_found_by_id")
                )
            
            # Проверка что вариант принадлежит товару из галереи
            if variant.product_id != self.model.product_id:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("product_variant_does_not_belong_to_product")
                )

        # Проверка существования файла по file_id (если указан новый)
        if dto.file_id is not None:
            if (await self.file_repository.get(dto.file_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("file_not_found_by_id")
                )

        # Валидация файла изображения (если предоставлен)
        if file:
            self.file_service.validate_file(file, self.extensions)

    async def transform(self, dto: ProductGalleryUpdateDTO, file: UploadFile | None = None):
        """
        Трансформирует данные перед обновлением изображения галереи товара.

        Args:
            dto (ProductGalleryUpdateDTO): DTO с данными для трансформации.
            file (UploadFile | None): Опциональный файл изображения для сохранения.
        """
        # Получение значения товара для папки загрузки
        product = await self.product_repository.get(self.model.product_id)
        self.upload_folder = AppFileExtensionConstants.product_image_directory(product.value)

        # Обработка файла изображения
        if file:
            if self.model.file_id:
                # Обновление существующего файла
                file_entity = await self.file_service.update_file(
                    file_id=self.model.file_id,
                    new_file=file,
                    uploaded_folder=self.upload_folder,
                    extensions=self.extensions,
                )
            else:
                # Создание нового файла
                file_entity = await self.file_service.save_file(
                    file, self.upload_folder, self.extensions
                )
            dto.file_id = file_entity.id