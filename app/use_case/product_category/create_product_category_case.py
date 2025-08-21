from fastapi import UploadFile
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


class CreateProductCategoryCase(BaseUseCase[ProductCategoryWithRelationsRDTO]):
    """
    Класс Use Case для создания новой категории товаров.

    Использует:
        - Репозиторий `ProductCategoryRepository` для работы с базой данных.
        - DTO `ProductCategoryCDTO` для входных данных.
        - DTO `ProductCategoryWithRelationsRDTO` для возврата данных с отношениями.
        - `FileService` для работы с изображениями.

    Атрибуты:
        repository (ProductCategoryRepository): Репозиторий для работы с категориями товаров.
        file_service (FileService): Сервис для работы с файлами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        model (ProductCategoryEntity | None): Модель категории товара для создания.

    Методы:
        execute(dto: ProductCategoryCDTO, file: UploadFile | None = None) -> ProductCategoryWithRelationsRDTO:
            Выполняет создание категории товара.
        validate(dto: ProductCategoryCDTO, file: UploadFile | None = None):
            Валидирует данные перед созданием.
        transform(dto: ProductCategoryCDTO, file: UploadFile | None = None):
            Трансформирует данные перед созданием.
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
        self, dto: ProductCategoryCDTO, file: UploadFile | None = None
    ) -> ProductCategoryWithRelationsRDTO:
        """
        Выполняет операцию создания новой категории товара.

        Args:
            dto (ProductCategoryCDTO): DTO с данными для создания категории товара.
            file (UploadFile | None): Опциональный файл изображения категории.

        Returns:
            ProductCategoryWithRelationsRDTO: Созданный объект категории товара с отношениями.

        Raises:
            AppExceptionResponse: Если категория с таким значением уже существует или файл не валиден.
        """
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        self.model = await self.repository.create(obj=self.model)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return ProductCategoryWithRelationsRDTO.from_orm(self.model)

    async def validate(self, dto: ProductCategoryCDTO, file: UploadFile | None = None) -> None:
        """
        Валидирует данные перед созданием категории товара.

        Args:
            dto (ProductCategoryCDTO): DTO с данными для валидации.
            file (UploadFile | None): Опциональный файл изображения для валидации.

        Raises:
            AppExceptionResponse: Если категория с таким значением уже существует, файл не валиден или изображение не найдено.
        """
        # Автогенерация value из title_ru если не предоставлено
        if dto.value is None:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Проверка уникальности значения
        existed = await self.repository.get_first_with_filters(
            filters=[self.repository.model.value == dto.value]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
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

    async def transform(self, dto: ProductCategoryCDTO, file: UploadFile | None = None):
        """
        Трансформирует данные перед созданием категории товара.

        Args:
            dto (ProductCategoryCDTO): DTO с данными для трансформации.
            file (UploadFile | None): Опциональный файл изображения для сохранения.
        """
        # Определение папки для загрузки изображений категорий
        self.upload_folder = f"product_categories/images/{dto.value}"

        # Сохранение файла если предоставлен
        if file:
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.image_id = file_entity.id

        # Создание модели для сохранения
        self.model = ProductCategoryEntity(**dto.dict())