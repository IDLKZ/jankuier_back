from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_variant_modification.product_variant_modification_dto import (
    ProductVariantModificationWithRelationsRDTO,
)
from app.adapters.repository.product_variant_modification.product_variant_modification_repository import (
    ProductVariantModificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductVariantModificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetProductVariantModificationByIdCase(
    BaseUseCase[ProductVariantModificationWithRelationsRDTO]
):
    """
    Класс Use Case для получения модификации варианта товара по ID.

    Использует:
        - Репозиторий `ProductVariantModificationRepository` для работы с базой данных.
        - DTO `ProductVariantModificationWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductVariantModificationRepository): Репозиторий для работы с модификациями вариантов товаров.
        model (ProductVariantModificationEntity | None): Найденная модель модификации варианта товара.

    Методы:
        execute(id: int) -> ProductVariantModificationWithRelationsRDTO:
            Выполняет поиск и возвращает модификацию варианта товара по ID.
        validate(id: int):
            Валидирует существование модификации варианта товара с данным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductVariantModificationRepository(db)
        self.model: ProductVariantModificationEntity | None = None

    async def execute(self, id: int) -> ProductVariantModificationWithRelationsRDTO:
        """
        Выполняет операцию получения модификации варианта товара по ID.

        Args:
            id (int): Идентификатор модификации варианта товара.

        Returns:
            ProductVariantModificationWithRelationsRDTO: Объект модификации варианта товара с отношениями.

        Raises:
            AppExceptionResponse: Если модификация варианта товара не найдена.
        """
        await self.validate(id=id)
        return ProductVariantModificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидирует существование модификации варианта товара с данным ID.

        Args:
            id (int): Идентификатор модификации варианта товара для поиска.

        Raises:
            AppExceptionResponse: Если модификация варианта товара не найдена.
        """
        self.model = await self.repository.get(
            id=id,
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
