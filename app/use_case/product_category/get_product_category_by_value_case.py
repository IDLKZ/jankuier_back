from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_category.product_category_dto import (
    ProductCategoryWithRelationsRDTO,
)
from app.adapters.repository.product_category.product_category_repository import (
    ProductCategoryRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductCategoryEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetProductCategoryByValueCase(BaseUseCase[ProductCategoryWithRelationsRDTO]):
    """
    Класс Use Case для получения категории товара по уникальному значению.

    Использует:
        - Репозиторий `ProductCategoryRepository` для работы с базой данных.
        - DTO `ProductCategoryWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductCategoryRepository): Репозиторий для работы с категориями товаров.
        model (ProductCategoryEntity | None): Найденная модель категории товара.

    Методы:
        execute(value: str) -> ProductCategoryWithRelationsRDTO:
            Выполняет поиск и возвращает категорию товара по уникальному значению.
        validate(value: str):
            Валидирует существование категории товара с данным значением.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductCategoryRepository(db)
        self.model: ProductCategoryEntity | None = None

    async def execute(self, value: str) -> ProductCategoryWithRelationsRDTO:
        """
        Выполняет операцию получения категории товара по уникальному значению.

        Args:
            value (str): Уникальное значение категории товара.

        Returns:
            ProductCategoryWithRelationsRDTO: Объект категории товара с отношениями.

        Raises:
            AppExceptionResponse: Если категория товара не найдена.
        """
        await self.validate(value=value)
        return ProductCategoryWithRelationsRDTO.from_orm(self.model)

    async def validate(self, value: str) -> None:
        """
        Валидирует существование категории товара с данным значением.

        Args:
            value (str): Уникальное значение категории товара для поиска.

        Raises:
            AppExceptionResponse: Если категория товара не найдена.
        """
        self.model = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == value.lower()],
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
