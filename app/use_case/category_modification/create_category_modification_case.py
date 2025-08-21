from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.category_modification.category_modification_dto import CategoryModificationCDTO, CategoryModificationWithRelationsRDTO
from app.adapters.repository.category_modification.category_modification_repository import CategoryModificationRepository
from app.adapters.repository.modification_type.modification_type_repository import ModificationTypeRepository
from app.adapters.repository.product_category.product_category_repository import ProductCategoryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CategoryModificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateCategoryModificationCase(BaseUseCase[CategoryModificationWithRelationsRDTO]):
    """
    Класс Use Case для создания новой модификации категории.

    Использует:
        - Репозиторий `CategoryModificationRepository` для работы с базой данных.
        - DTO `CategoryModificationCDTO` для входных данных.
        - DTO `CategoryModificationWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (CategoryModificationRepository): Репозиторий для работы с модификациями категорий.
        product_category_repository (ProductCategoryRepository): Репозиторий для работы с категориями товаров.
        modification_type_repository (ModificationTypeRepository): Репозиторий для работы с типами модификаций.
        model (CategoryModificationEntity | None): Модель модификации категории для создания.

    Методы:
        execute(dto: CategoryModificationCDTO) -> CategoryModificationWithRelationsRDTO:
            Выполняет создание модификации категории.
        validate(dto: CategoryModificationCDTO):
            Валидирует данные перед созданием.
        transform(dto: CategoryModificationCDTO):
            Трансформирует данные перед созданием.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CategoryModificationRepository(db)
        self.product_category_repository = ProductCategoryRepository(db)
        self.modification_type_repository = ModificationTypeRepository(db)
        self.model: CategoryModificationEntity | None = None

    async def execute(self, dto: CategoryModificationCDTO) -> CategoryModificationWithRelationsRDTO:
        """
        Выполняет операцию создания новой модификации категории.

        Args:
            dto (CategoryModificationCDTO): DTO с данными для создания модификации категории.

        Returns:
            CategoryModificationWithRelationsRDTO: Созданный объект модификации категории с отношениями.

        Raises:
            AppExceptionResponse: Если связанные сущности не найдены, дублирование или валидация не прошла.
        """
        await self.validate(dto=dto)
        await self.transform(dto=dto)
        self.model = await self.repository.create(obj=self.model)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return CategoryModificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self, dto: CategoryModificationCDTO) -> None:
        """
        Валидирует данные перед созданием модификации категории.

        Args:
            dto (CategoryModificationCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если связанные сущности не найдены или модификация уже существует.
        """
        # Проверка существования категории товара
        if (await self.product_category_repository.get(dto.category_id)) is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_category_not_found_by_id")
            )

        # Проверка существования типа модификации (если указан)
        if dto.modification_type_id is not None:
            if (await self.modification_type_repository.get(dto.modification_type_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("modification_type_not_found_by_id")
                )

        # Проверка на дублирование связи (одна категория не может иметь одинаковые типы модификаций)
        filters = [self.repository.model.category_id == dto.category_id]
        
        if dto.modification_type_id is not None:
            filters.append(self.repository.model.modification_type_id == dto.modification_type_id)
        else:
            filters.append(self.repository.model.modification_type_id.is_(None))

        existed = await self.repository.get_first_with_filters(filters=filters)
        if existed:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("category_modification_already_exists")
            )

    async def transform(self, dto: CategoryModificationCDTO):
        """
        Трансформирует данные перед созданием модификации категории.

        Args:
            dto (CategoryModificationCDTO): DTO с данными для трансформации.
        """
        # Создание модели для сохранения
        self.model = CategoryModificationEntity(**dto.dict())