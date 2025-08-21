from fastapi import UploadFile
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product.product_dto import ProductCDTO, ProductWithRelationsRDTO
from app.adapters.repository.city.city_repository import CityRepository
from app.adapters.repository.file.file_repository import FileRepository
from app.adapters.repository.product.product_repository import ProductRepository
from app.adapters.repository.product_category.product_category_repository import (
    ProductCategoryRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CreateProductCase(BaseUseCase[ProductWithRelationsRDTO]):
    """
    Класс Use Case для создания нового товара.

    Использует:
        - Репозиторий `ProductRepository` для работы с базой данных.
        - DTO `ProductCDTO` для входных данных.
        - DTO `ProductWithRelationsRDTO` для возврата данных с отношениями.
        - `FileService` для работы с изображениями.

    Атрибуты:
        repository (ProductRepository): Репозиторий для работы с товарами.
        city_repository (CityRepository): Репозиторий для работы с городами.
        category_repository (ProductCategoryRepository): Репозиторий для работы с категориями.
        file_service (FileService): Сервис для работы с файлами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        model (ProductEntity | None): Модель товара для создания.

    Методы:
        execute(dto: ProductCDTO, file: UploadFile | None = None) -> ProductWithRelationsRDTO:
            Выполняет создание товара.
        validate(dto: ProductCDTO, file: UploadFile | None = None):
            Валидирует данные перед созданием.
        transform(dto: ProductCDTO, file: UploadFile | None = None):
            Трансформирует данные перед созданием.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductRepository(db)
        self.city_repository = CityRepository(db)
        self.category_repository = ProductCategoryRepository(db)
        self.file_service = FileService(db)
        self.file_repository = FileRepository(db)
        self.model: ProductEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, dto: ProductCDTO, file: UploadFile | None = None
    ) -> ProductWithRelationsRDTO:
        """
        Выполняет операцию создания нового товара.

        Args:
            dto (ProductCDTO): DTO с данными для создания товара.
            file (UploadFile | None): Опциональный файл изображения товара.

        Returns:
            ProductWithRelationsRDTO: Созданный объект товара с отношениями.

        Raises:
            AppExceptionResponse: Если товар с таким значением/SKU уже существует или валидация не прошла.
        """
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        self.model = await self.repository.create(obj=self.model)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return ProductWithRelationsRDTO.from_orm(self.model)

    async def validate(self, dto: ProductCDTO, file: UploadFile | None = None) -> None:
        """
        Валидирует данные перед созданием товара.

        Args:
            dto (ProductCDTO): DTO с данными для валидации.
            file (UploadFile | None): Опциональный файл изображения для валидации.

        Raises:
            AppExceptionResponse: Если товар с таким значением/SKU уже существует, связанные сущности не найдены или файл не валиден.
        """
        # Автогенерация value из title_ru если не предоставлено
        if dto.value is None:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Проверка уникальности value и sku
        existed = await self.repository.get_first_with_filters(
            filters=[
                or_(
                    self.repository.model.value == dto.value,
                    self.repository.model.sku == dto.sku,
                )
            ]
        )
        if existed:
            if existed.value == dto.value:
                raise AppExceptionResponse.bad_request(
                    message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
                )
            if existed.sku == dto.sku:
                raise AppExceptionResponse.bad_request(
                    message=f"{i18n.gettext('sku_already_exists')}{dto.sku}"
                )

        # Проверка существования города
        if dto.city_id:
            if (await self.city_repository.get(dto.city_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("city_not_found_by_id")
                )

        # Проверка существования категории
        if dto.category_id:
            if (await self.category_repository.get(dto.category_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("category_not_found_by_id")
                )

        # Валидация файла изображения
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла по image_id
        if dto.image_id:
            if (await self.file_repository.get(dto.image_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("image_not_found_by_id")
                )

    async def transform(self, dto: ProductCDTO, file: UploadFile | None = None):
        """
        Трансформирует данные перед созданием товара.

        Args:
            dto (ProductCDTO): DTO с данными для трансформации.
            file (UploadFile | None): Опциональный файл изображения для сохранения.
        """
        # Определение папки для загрузки изображений товаров с использованием helper функции
        self.upload_folder = AppFileExtensionConstants.product_image_directory(
            dto.value
        )

        # Сохранение файла если предоставлен
        if file:
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.image_id = file_entity.id

        # Создание модели для сохранения
        self.model = ProductEntity(**dto.dict())
