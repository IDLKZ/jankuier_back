from fastapi import UploadFile
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_variant.product_variant_dto import ProductVariantCDTO, ProductVariantWithRelationsRDTO
from app.adapters.repository.city.city_repository import CityRepository
from app.adapters.repository.file.file_repository import FileRepository
from app.adapters.repository.product.product_repository import ProductRepository
from app.adapters.repository.product_variant.product_variant_repository import ProductVariantRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductVariantEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CreateProductVariantCase(BaseUseCase[ProductVariantWithRelationsRDTO]):
    """
    Класс Use Case для создания нового варианта товара.

    Использует:
        - Репозиторий `ProductVariantRepository` для работы с базой данных.
        - DTO `ProductVariantCDTO` для входных данных.
        - DTO `ProductVariantWithRelationsRDTO` для возврата данных с отношениями.
        - `FileService` для работы с изображениями.

    Атрибуты:
        repository (ProductVariantRepository): Репозиторий для работы с вариантами товаров.
        product_repository (ProductRepository): Репозиторий для работы с товарами.
        city_repository (CityRepository): Репозиторий для работы с городами.
        file_service (FileService): Сервис для работы с файлами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        model (ProductVariantEntity | None): Модель варианта товара для создания.

    Методы:
        execute(dto: ProductVariantCDTO, file: UploadFile | None = None) -> ProductVariantWithRelationsRDTO:
            Выполняет создание варианта товара.
        validate(dto: ProductVariantCDTO, file: UploadFile | None = None):
            Валидирует данные перед созданием.
        transform(dto: ProductVariantCDTO, file: UploadFile | None = None):
            Трансформирует данные перед созданием.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductVariantRepository(db)
        self.product_repository = ProductRepository(db)
        self.city_repository = CityRepository(db)
        self.file_service = FileService(db)
        self.file_repository = FileRepository(db)
        self.model: ProductVariantEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, dto: ProductVariantCDTO, file: UploadFile | None = None
    ) -> ProductVariantWithRelationsRDTO:
        """
        Выполняет операцию создания нового варианта товара.

        Args:
            dto (ProductVariantCDTO): DTO с данными для создания варианта товара.
            file (UploadFile | None): Опциональный файл изображения варианта.

        Returns:
            ProductVariantWithRelationsRDTO: Созданный объект варианта товара с отношениями.

        Raises:
            AppExceptionResponse: Если вариант с таким значением/SKU уже существует или валидация не прошла.
        """
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        self.model = await self.repository.create(obj=self.model)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return ProductVariantWithRelationsRDTO.from_orm(self.model)

    async def validate(self, dto: ProductVariantCDTO, file: UploadFile | None = None) -> None:
        """
        Валидирует данные перед созданием варианта товара.

        Args:
            dto (ProductVariantCDTO): DTO с данными для валидации.
            file (UploadFile | None): Опциональный файл изображения для валидации.

        Raises:
            AppExceptionResponse: Если вариант с таким значением/SKU уже существует, связанные сущности не найдены или файл не валиден.
        """
        # Автогенерация value из title_ru если не предоставлено
        if dto.value is None:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Проверка уникальности value и sku (если указан)
        filters = [self.repository.model.value == dto.value]
        if dto.sku is not None:
            filters.append(self.repository.model.sku == dto.sku)

        existed = await self.repository.get_first_with_filters(
            filters=[or_(*filters)]
        )
        if existed:
            if existed.value == dto.value:
                raise AppExceptionResponse.bad_request(
                    message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
                )
            if dto.sku is not None and existed.sku == dto.sku:
                raise AppExceptionResponse.bad_request(
                    message=f"{i18n.gettext('sku_already_exists')}{dto.sku}"
                )

        # Проверка существования товара
        if (await self.product_repository.get(dto.product_id)) is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_not_found_by_id")
            )

        # Проверка существования города (если указан)
        if dto.city_id:
            if (await self.city_repository.get(dto.city_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("city_not_found_by_id")
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

    async def transform(self, dto: ProductVariantCDTO, file: UploadFile | None = None):
        """
        Трансформирует данные перед созданием варианта товара.

        Args:
            dto (ProductVariantCDTO): DTO с данными для трансформации.
            file (UploadFile | None): Опциональный файл изображения для сохранения.
        """
        # Определение папки для загрузки изображений вариантов товаров
        self.upload_folder = f"{AppFileExtensionConstants.ProductFolderName}/variants/{dto.value}"

        # Сохранение файла если предоставлен
        if file:
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.image_id = file_entity.id

        # Создание модели для сохранения
        self.model = ProductVariantEntity(**dto.dict())