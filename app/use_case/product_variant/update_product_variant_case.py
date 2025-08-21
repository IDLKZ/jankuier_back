from fastapi import UploadFile
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_variant.product_variant_dto import ProductVariantUpdateDTO, ProductVariantWithRelationsRDTO
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


class UpdateProductVariantCase(BaseUseCase[ProductVariantWithRelationsRDTO]):
    """
    Класс Use Case для обновления варианта товара.

    Использует:
        - Репозиторий `ProductVariantRepository` для работы с базой данных.
        - DTO `ProductVariantUpdateDTO` для входных данных.
        - DTO `ProductVariantWithRelationsRDTO` для возврата данных с отношениями.
        - `FileService` для работы с изображениями.

    Атрибуты:
        repository (ProductVariantRepository): Репозиторий для работы с вариантами товаров.
        product_repository (ProductRepository): Репозиторий для работы с товарами.
        city_repository (CityRepository): Репозиторий для работы с городами.
        file_service (FileService): Сервис для работы с файлами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        model (ProductVariantEntity | None): Модель варианта товара для обновления.

    Методы:
        execute(id: int, dto: ProductVariantUpdateDTO, file: UploadFile | None = None) -> ProductVariantWithRelationsRDTO:
            Выполняет обновление варианта товара.
        validate(id: int, dto: ProductVariantUpdateDTO, file: UploadFile | None = None):
            Валидирует данные перед обновлением.
        transform(dto: ProductVariantUpdateDTO, file: UploadFile | None = None):
            Трансформирует данные перед обновлением.
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
        self, id: int, dto: ProductVariantUpdateDTO, file: UploadFile | None = None
    ) -> ProductVariantWithRelationsRDTO:
        """
        Выполняет операцию обновления варианта товара.

        Args:
            id (int): Идентификатор варианта товара для обновления.
            dto (ProductVariantUpdateDTO): DTO с данными для обновления варианта товара.
            file (UploadFile | None): Опциональный файл изображения варианта.

        Returns:
            ProductVariantWithRelationsRDTO: Обновленный объект варианта товара с отношениями.

        Raises:
            AppExceptionResponse: Если вариант не найден, значение/SKU уже существует или валидация не прошла.
        """
        await self.validate(id=id, dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        self.model = await self.repository.update(obj=self.model, dto=dto)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return ProductVariantWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, dto: ProductVariantUpdateDTO, file: UploadFile | None = None) -> None:
        """
        Валидирует данные перед обновлением варианта товара.

        Args:
            id (int): Идентификатор варианта товара для обновления.
            dto (ProductVariantUpdateDTO): DTO с данными для валидации.
            file (UploadFile | None): Опциональный файл изображения для валидации.

        Raises:
            AppExceptionResponse: Если вариант не найден, значение/SKU уже существует, связанные сущности не найдены или файл не валиден.
        """
        # Проверка существования варианта товара
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Автогенерация value из title_ru если указан title_ru но не указан value
        if dto.title_ru is not None and dto.value is None:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Проверка уникальности value и sku (если указаны и изменились)
        filters = []
        
        if dto.value is not None and dto.value != self.model.value:
            filters.append(self.repository.model.value == dto.value)
        
        if dto.sku is not None and dto.sku != self.model.sku:
            filters.append(self.repository.model.sku == dto.sku)

        if filters:
            # Исключаем текущую запись из проверки
            filters.append(self.repository.model.id != id)
            
            existed = await self.repository.get_first_with_filters(
                filters=[or_(*filters)]
            )
            if existed:
                if dto.value is not None and existed.value == dto.value:
                    raise AppExceptionResponse.bad_request(
                        message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
                    )
                if dto.sku is not None and existed.sku == dto.sku:
                    raise AppExceptionResponse.bad_request(
                        message=f"{i18n.gettext('sku_already_exists')}{dto.sku}"
                    )

        # Проверка существования товара (если указан новый)
        if dto.product_id is not None:
            if (await self.product_repository.get(dto.product_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("product_not_found_by_id")
                )

        # Проверка существования города (если указан новый)
        if dto.city_id is not None:
            if (await self.city_repository.get(dto.city_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("city_not_found_by_id")
                )

        # Валидация файла изображения
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла по image_id (если указан новый)
        if dto.image_id is not None:
            if (await self.file_repository.get(dto.image_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("image_not_found_by_id")
                )

    async def transform(self, dto: ProductVariantUpdateDTO, file: UploadFile | None = None):
        """
        Трансформирует данные перед обновлением варианта товара.

        Args:
            dto (ProductVariantUpdateDTO): DTO с данными для трансформации.
            file (UploadFile | None): Опциональный файл изображения для сохранения.
        """
        # Определение папки для загрузки изображений вариантов товаров
        variant_value = dto.value if dto.value is not None else self.model.value
        self.upload_folder = f"{AppFileExtensionConstants.ProductFolderName}/variants/{variant_value}"

        # Обработка файла изображения
        if file:
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
                    file, self.upload_folder, self.extensions
                )
            dto.image_id = file_entity.id