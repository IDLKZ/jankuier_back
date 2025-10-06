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


class GetProductCategoryByIdCase(BaseUseCase[ProductCategoryWithRelationsRDTO]):
    """
    Класс Use Case для получения категории товара по ID.

    Использует:
        - Репозиторий `ProductCategoryRepository` для работы с базой данных.
        - DTO `ProductCategoryWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductCategoryRepository): Репозиторий для работы с категориями товаров.
        model (ProductCategoryEntity | None): Найденная модель категории товара.

    Методы:
        execute(id: int) -> ProductCategoryWithRelationsRDTO:
            Выполняет поиск и возвращает категорию товара по ID.
        validate(id: int):
            Валидирует существование категории товара с данным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductCategoryRepository(db)
        self.model: ProductCategoryEntity | None = None

    async def execute(self, id: int) -> ProductCategoryWithRelationsRDTO:
        """
        Выполняет операцию получения категории товара по ID.

        Args:
            id (int): Идентификатор категории товара.

        Returns:
            ProductCategoryWithRelationsRDTO: Объект категории товара с отношениями.

        Raises:
            AppExceptionResponse: Если категория товара не найдена.
        """
        await self.validate(id=id)
        return ProductCategoryWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидирует существование категории товара с данным ID.

        Args:
            id (int): Идентификатор категории товара для поиска.

        Raises:
            AppExceptionResponse: Если категория товара не найдена.
        """
        self.model = await self.repository.get(
            id=id,
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
