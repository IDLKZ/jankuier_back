from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_variant_modification.product_variant_modification_dto import ProductVariantModificationCDTO, ProductVariantModificationWithRelationsRDTO
from app.adapters.repository.modification_value.modification_value_repository import ModificationValueRepository
from app.adapters.repository.product_variant.product_variant_repository import ProductVariantRepository
from app.adapters.repository.product_variant_modification.product_variant_modification_repository import ProductVariantModificationRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductVariantModificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateProductVariantModificationCase(BaseUseCase[ProductVariantModificationWithRelationsRDTO]):
    """
    Класс Use Case для создания новой модификации варианта товара.

    Использует:
        - Репозиторий `ProductVariantModificationRepository` для работы с базой данных.
        - DTO `ProductVariantModificationCDTO` для входных данных.
        - DTO `ProductVariantModificationWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductVariantModificationRepository): Репозиторий для работы с модификациями вариантов товаров.
        product_variant_repository (ProductVariantRepository): Репозиторий для работы с вариантами товаров.
        modification_value_repository (ModificationValueRepository): Репозиторий для работы со значениями модификаций.
        model (ProductVariantModificationEntity | None): Модель модификации варианта товара для создания.

    Методы:
        execute(dto: ProductVariantModificationCDTO) -> ProductVariantModificationWithRelationsRDTO:
            Выполняет создание модификации варианта товара.
        validate(dto: ProductVariantModificationCDTO):
            Валидирует данные перед созданием.
        transform(dto: ProductVariantModificationCDTO):
            Трансформирует данные перед созданием.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductVariantModificationRepository(db)
        self.product_variant_repository = ProductVariantRepository(db)
        self.modification_value_repository = ModificationValueRepository(db)
        self.model: ProductVariantModificationEntity | None = None

    async def execute(self, dto: ProductVariantModificationCDTO) -> ProductVariantModificationWithRelationsRDTO:
        """
        Выполняет операцию создания новой модификации варианта товара.

        Args:
            dto (ProductVariantModificationCDTO): DTO с данными для создания модификации варианта товара.

        Returns:
            ProductVariantModificationWithRelationsRDTO: Созданный объект модификации варианта товара с отношениями.

        Raises:
            AppExceptionResponse: Если связанные сущности не найдены, дублирование или валидация не прошла.
        """
        await self.validate(dto=dto)
        await self.transform(dto=dto)
        self.model = await self.repository.create(obj=self.model)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return ProductVariantModificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self, dto: ProductVariantModificationCDTO) -> None:
        """
        Валидирует данные перед созданием модификации варианта товара.

        Args:
            dto (ProductVariantModificationCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если связанные сущности не найдены или модификация уже существует.
        """
        # Проверка существования варианта товара
        if (await self.product_variant_repository.get(dto.variant_id)) is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_variant_not_found_by_id")
            )

        # Проверка существования значения модификации
        if (await self.modification_value_repository.get(dto.modification_value_id)) is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("modification_value_not_found_by_id")
            )

        # Проверка на дублирование связи (один вариант не может иметь одинаковые модификации)
        existed = await self.repository.get_first_with_filters(
            filters=[
                self.repository.model.variant_id == dto.variant_id,
                self.repository.model.modification_value_id == dto.modification_value_id
            ]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_variant_modification_already_exists")
            )

    async def transform(self, dto: ProductVariantModificationCDTO):
        """
        Трансформирует данные перед созданием модификации варианта товара.

        Args:
            dto (ProductVariantModificationCDTO): DTO с данными для трансформации.
        """
        # Создание модели для сохранения
        self.model = ProductVariantModificationEntity(**dto.dict())