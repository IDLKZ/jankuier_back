from fastapi import UploadFile
from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product.product_dto import (
    ProductUpdateDTO,
    ProductWithRelationsRDTO,
)
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


class UpdateProductCase(BaseUseCase[ProductWithRelationsRDTO]):
    """
    Класс Use Case для обновления товара.

    Использует:
        - Репозиторий `ProductRepository` для работы с базой данных.
        - DTO `ProductUpdateDTO` для входных данных.
        - DTO `ProductWithRelationsRDTO` для возврата данных с отношениями.
        - `FileService` для работы с изображениями.

    Атрибуты:
        repository (ProductRepository): Репозиторий для работы с товарами.
        city_repository (CityRepository): Репозиторий для работы с городами.
        category_repository (ProductCategoryRepository): Репозиторий для работы с категориями.
        file_service (FileService): Сервис для работы с файлами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        model (ProductEntity | None): Модель товара для обновления.

    Методы:
        execute(id: int, dto: ProductUpdateDTO, file: UploadFile | None = None) -> ProductWithRelationsRDTO:
            Выполняет обновление товара.
        validate(id: int, dto: ProductUpdateDTO, file: UploadFile | None = None):
            Валидирует данные перед обновлением.
        transform(dto: ProductUpdateDTO, file: UploadFile | None = None):
            Трансформирует данные перед обновлением.
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
        self, id: int, dto: ProductUpdateDTO, file: UploadFile | None = None
    ) -> ProductWithRelationsRDTO:
        """
        Выполняет операцию обновления товара.

        Args:
            id (int): Идентификатор товара.
            dto (ProductUpdateDTO): DTO с данными для обновления.
            file (UploadFile | None): Опциональный файл изображения товара.

        Returns:
            ProductWithRelationsRDTO: Обновленный объект товара с отношениями.

        Raises:
            AppExceptionResponse: Если товар не найден, значение/SKU уже существует или файл не валиден.
        """
        await self.validate(id=id, dto=dto, file=file)
        dto = await self.transform(dto=dto, file=file)
        self.model = await self.repository.update(obj=self.model, dto=dto)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return ProductWithRelationsRDTO.from_orm(self.model)

    async def validate(
        self, id: int, dto: ProductUpdateDTO, file: UploadFile | None = None
    ) -> None:
        """
        Валидирует данные перед обновлением товара.

        Args:
            id (int): Идентификатор товара.
            dto (ProductUpdateDTO): DTO с данными для валидации.
            file (UploadFile | None): Опциональный файл изображения для валидации.

        Raises:
            AppExceptionResponse: Если товар не найден, значение/SKU уже существует, связанные сущности не найдены или файл не валиден.
        """
        # Проверка существования товара
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))

        # Автогенерация value из title_ru если обновляется и не предоставлено
        if dto.title_ru is not None and dto.value is None:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Проверка уникальности value и sku (исключая текущую запись)
        if dto.value is not None or hasattr(dto, "sku") and dto.sku is not None:
            filters = []
            if dto.value is not None:
                filters.append(self.repository.model.value == dto.value)
            if hasattr(dto, "sku") and dto.sku is not None:
                filters.append(self.repository.model.sku == dto.sku)

            if filters:
                existed = await self.repository.get_first_with_filters(
                    filters=[and_(self.repository.model.id != id, or_(*filters))],
                    include_deleted_filter=True,
                )
                if existed:
                    if dto.value is not None and existed.value == dto.value:
                        raise AppExceptionResponse.bad_request(
                            message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
                        )
                    if (
                        hasattr(dto, "sku")
                        and dto.sku is not None
                        and existed.sku == dto.sku
                    ):
                        raise AppExceptionResponse.bad_request(
                            message=f"{i18n.gettext('sku_already_exists')}{dto.sku}"
                        )

        # Проверка существования города (если обновляется)
        if dto.city_id is not None:
            if (await self.city_repository.get(dto.city_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("city_not_found_by_id")
                )

        # Проверка существования категории (если обновляется)
        if dto.category_id is not None:
            if (await self.category_repository.get(dto.category_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("category_not_found_by_id")
                )

        # Валидация файла изображения
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла по image_id (если изменился)
        if dto.image_id is not None and self.model.image_id != dto.image_id:
            if (await self.file_repository.get(dto.image_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("image_not_found_by_id")
                )

    async def transform(
        self, dto: ProductUpdateDTO, file: UploadFile | None = None
    ) -> ProductUpdateDTO:
        """
        Трансформирует данные перед обновлением товара.

        Args:
            dto (ProductUpdateDTO): DTO с данными для трансформации.
            file (UploadFile | None): Опциональный файл изображения для обновления.

        Returns:
            ProductUpdateDTO: Трансформированный DTO.
        """
        # Определение папки для загрузки изображений товаров
        current_value = dto.value if dto.value is not None else self.model.value
        self.upload_folder = AppFileExtensionConstants.product_image_directory(
            current_value
        )

        # Обработка файла изображения
        if file:
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
            dto.image_id = file_entity.id

        return dto
