from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product.product_dto import ProductWithRelationsRDTO
from app.adapters.repository.product.product_repository import ProductRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetProductByValueCase(BaseUseCase[ProductWithRelationsRDTO]):
    """
    Класс Use Case для получения товара по уникальному значению.

    Использует:
        - Репозиторий `ProductRepository` для работы с базой данных.
        - DTO `ProductWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductRepository): Репозиторий для работы с товарами.
        model (ProductEntity | None): Найденная модель товара.

    Методы:
        execute(value: str) -> ProductWithRelationsRDTO:
            Выполняет поиск и возвращает товар по уникальному значению.
        validate(value: str):
            Валидирует существование товара с данным значением.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductRepository(db)
        self.model: ProductEntity | None = None

    async def execute(self, value: str) -> ProductWithRelationsRDTO:
        """
        Выполняет операцию получения товара по уникальному значению.

        Args:
            value (str): Уникальное значение товара.

        Returns:
            ProductWithRelationsRDTO: Объект товара с отношениями.

        Raises:
            AppExceptionResponse: Если товар не найден.
        """
        await self.validate(value=value)
        return ProductWithRelationsRDTO.from_orm(self.model)

    async def validate(self, value: str) -> None:
        """
        Валидирует существование товара с данным значением.

        Args:
            value (str): Уникальное значение товара для поиска.

        Raises:
            AppExceptionResponse: Если товар не найден.
        """
        self.model = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == value.lower()],
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
