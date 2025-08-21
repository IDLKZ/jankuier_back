from fastapi import UploadFile
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_category.product_category_dto import ProductCategoryCDTO, ProductCategoryWithRelationsRDTO
from app.adapters.repository.file.file_repository import FileRepository
from app.adapters.repository.product_category.product_category_repository import ProductCategoryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductCategoryEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class UpdateProductCategoryCase(BaseUseCase[ProductCategoryWithRelationsRDTO]):
    """
    Класс Use Case для обновления категории товаров.

    Использует:
        - Репозиторий `ProductCategoryRepository` для работы с базой данных.
        - DTO `ProductCategoryCDTO` для входных данных.
        - DTO `ProductCategoryWithRelationsRDTO` для возврата данных с отношениями.
        - `FileService` для работы с изображениями.

    Атрибуты:
        repository (ProductCategoryRepository): Репозиторий для работы с категориями товаров.
        file_service (FileService): Сервис для работы с файлами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        model (ProductCategoryEntity | None): Модель категории товара для обновления.

    Методы:
        execute(id: int, dto: ProductCategoryCDTO, file: UploadFile | None = None) -> ProductCategoryWithRelationsRDTO:
            Выполняет обновление категории товара.
        validate(id: int, dto: ProductCategoryCDTO, file: UploadFile | None = None):
            Валидирует данные перед обновлением.
        transform(dto: ProductCategoryCDTO, file: UploadFile | None = None):
            Трансформирует данные перед обновлением.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductCategoryRepository(db)
        self.file_service = FileService(db)
        self.file_repository = FileRepository(db)
        self.model: ProductCategoryEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, id: int, dto: ProductCategoryCDTO, file: UploadFile | None = None
    ) -> ProductCategoryWithRelationsRDTO:
        """
        Выполняет операцию обновления категории товара.

        Args:
            id (int): Идентификатор категории товара.
            dto (ProductCategoryCDTO): DTO с данными для обновления.
            file (UploadFile | None): Опциональный файл изображения категории.

        Returns:
            ProductCategoryWithRelationsRDTO: Обновленный объект категории товара с отношениями.

        Raises:
            AppExceptionResponse: Если категория не найдена, значение уже существует или файл не валиден.
        """
        await self.validate(id=id, dto=dto, file=file)
        dto = await self.transform(dto=dto, file=file)
        self.model = await self.repository.update(obj=self.model, dto=dto)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return ProductCategoryWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, dto: ProductCategoryCDTO, file: UploadFile | None = None) -> None:
        """
        Валидирует данные перед обновлением категории товара.

        Args:
            id (int): Идентификатор категории товара.
            dto (ProductCategoryCDTO): DTO с данными для валидации.
            file (UploadFile | None): Опциональный файл изображения для валидации.

        Raises:
            AppExceptionResponse: Если категория не найдена, значение уже существует, файл не валиден или изображение не найдено.
        """
        # Проверка существования категории товара
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Автогенерация value из title_ru если не предоставлено
        if dto.value is None:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Проверка уникальности значения (исключая текущую запись)
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id != id,
                    self.repository.model.value == dto.value,
                )
            ],
            include_deleted_filter=True,
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
            )

        # Валидация файла изображения
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла по image_id (если изменился)
        if dto.image_id and self.model.image_id != dto.image_id:
            if (await self.file_repository.get(dto.image_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("image_not_found_by_id")
                )

    async def transform(self, dto: ProductCategoryCDTO, file: UploadFile | None = None) -> ProductCategoryCDTO:
        """
        Трансформирует данные перед обновлением категории товара.

        Args:
            dto (ProductCategoryCDTO): DTO с данными для трансформации.
            file (UploadFile | None): Опциональный файл изображения для обновления.

        Returns:
            ProductCategoryCDTO: Трансформированный DTO.
        """
        # Определение папки для загрузки изображений категорий
        self.upload_folder = f"product_categories/images/{dto.value}"

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