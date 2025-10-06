from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_variant.product_variant_dto import (
    ProductVariantWithRelationsRDTO,
)
from app.adapters.repository.product_variant.product_variant_repository import (
    ProductVariantRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductVariantEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetProductVariantByValueCase(BaseUseCase[ProductVariantWithRelationsRDTO]):
    """
    Класс Use Case для получения варианта товара по уникальному значению.

    Использует:
        - Репозиторий `ProductVariantRepository` для работы с базой данных.
        - DTO `ProductVariantWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductVariantRepository): Репозиторий для работы с вариантами товаров.
        model (ProductVariantEntity | None): Найденная модель варианта товара.

    Методы:
        execute(value: str) -> ProductVariantWithRelationsRDTO:
            Выполняет поиск и возвращает вариант товара по уникальному значению.
        validate(value: str):
            Валидирует существование варианта товара с данным значением.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductVariantRepository(db)
        self.model: ProductVariantEntity | None = None

    async def execute(self, value: str) -> ProductVariantWithRelationsRDTO:
        """
        Выполняет операцию получения варианта товара по уникальному значению.

        Args:
            value (str): Уникальное значение варианта товара.

        Returns:
            ProductVariantWithRelationsRDTO: Объект варианта товара с отношениями.

        Raises:
            AppExceptionResponse: Если вариант товара не найден.
        """
        await self.validate(value=value)
        return ProductVariantWithRelationsRDTO.from_orm(self.model)

    async def validate(self, value: str) -> None:
        """
        Валидирует существование варианта товара с данным значением.

        Args:
            value (str): Уникальное значение варианта товара для поиска.

        Raises:
            AppExceptionResponse: Если вариант товара не найден.
        """
        self.model = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == value.lower()],
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
