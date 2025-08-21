from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.category_modification.category_modification_dto import (
    CategoryModificationCDTO,
    CategoryModificationWithRelationsRDTO,
)
from app.adapters.repository.category_modification.category_modification_repository import (
    CategoryModificationRepository,
)
from app.adapters.repository.modification_type.modification_type_repository import (
    ModificationTypeRepository,
)
from app.adapters.repository.product_category.product_category_repository import (
    ProductCategoryRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CategoryModificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateCategoryModificationCase(
    BaseUseCase[CategoryModificationWithRelationsRDTO]
):
    """
    Класс Use Case для обновления модификации категории.

    Использует:
        - Репозиторий `CategoryModificationRepository` для работы с базой данных.
        - DTO `CategoryModificationCDTO` для входных данных.
        - DTO `CategoryModificationWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (CategoryModificationRepository): Репозиторий для работы с модификациями категорий.
        product_category_repository (ProductCategoryRepository): Репозиторий для работы с категориями товаров.
        modification_type_repository (ModificationTypeRepository): Репозиторий для работы с типами модификаций.
        model (CategoryModificationEntity | None): Модель модификации категории для обновления.

    Методы:
        execute(id: int, dto: CategoryModificationCDTO) -> CategoryModificationWithRelationsRDTO:
            Выполняет обновление модификации категории.
        validate(id: int, dto: CategoryModificationCDTO):
            Валидирует данные перед обновлением.
        transform(dto: CategoryModificationCDTO):
            Трансформирует данные перед обновлением.
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

    async def execute(
        self, id: int, dto: CategoryModificationCDTO
    ) -> CategoryModificationWithRelationsRDTO:
        """
        Выполняет операцию обновления модификации категории.

        Args:
            id (int): Идентификатор модификации категории для обновления.
            dto (CategoryModificationCDTO): DTO с данными для обновления модификации категории.

        Returns:
            CategoryModificationWithRelationsRDTO: Обновленный объект модификации категории с отношениями.

        Raises:
            AppExceptionResponse: Если модификация не найдена, связанные сущности не найдены или валидация не прошла.
        """
        await self.validate(id=id, dto=dto)
        await self.transform(dto=dto)
        self.model = await self.repository.update(obj=self.model, dto=dto)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return CategoryModificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, dto: CategoryModificationCDTO) -> None:
        """
        Валидирует данные перед обновлением модификации категории.

        Args:
            id (int): Идентификатор модификации категории для обновления.
            dto (CategoryModificationCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если модификация не найдена, связанные сущности не найдены или дублирование.
        """
        # Проверка существования модификации категории
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Проверка существования категории товара
        if (await self.product_category_repository.get(dto.category_id)) is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_category_not_found_by_id")
            )

        # Проверка существования типа модификации (если указан)
        if dto.modification_type_id is not None:
            if (
                await self.modification_type_repository.get(dto.modification_type_id)
            ) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("modification_type_not_found_by_id")
                )

        # Проверка на дублирование связи (исключая текущую запись)
        filters = [
            self.repository.model.category_id == dto.category_id,
            self.repository.model.id != id,
        ]

        if dto.modification_type_id is not None:
            filters.append(
                self.repository.model.modification_type_id == dto.modification_type_id
            )
        else:
            filters.append(self.repository.model.modification_type_id.is_(None))

        existed = await self.repository.get_first_with_filters(filters=filters)
        if existed:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("category_modification_already_exists")
            )

    async def transform(self, dto: CategoryModificationCDTO):
        """
        Трансформирует данные перед обновлением модификации категории.

        Args:
            dto (CategoryModificationCDTO): DTO с данными для трансформации.
        """
        # Трансформация не требуется для этой простой связующей сущности
        pass
