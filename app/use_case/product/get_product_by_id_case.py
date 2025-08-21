from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product.product_dto import ProductWithRelationsRDTO
from app.adapters.repository.product.product_repository import ProductRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetProductByIdCase(BaseUseCase[ProductWithRelationsRDTO]):
    """
    Класс Use Case для получения товара по ID.

    Использует:
        - Репозиторий `ProductRepository` для работы с базой данных.
        - DTO `ProductWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductRepository): Репозиторий для работы с товарами.
        model (ProductEntity | None): Найденная модель товара.

    Методы:
        execute(id: int) -> ProductWithRelationsRDTO:
            Выполняет поиск и возвращает товар по ID.
        validate(id: int):
            Валидирует существование товара с данным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductRepository(db)
        self.model: ProductEntity | None = None

    async def execute(self, id: int) -> ProductWithRelationsRDTO:
        """
        Выполняет операцию получения товара по ID.

        Args:
            id (int): Идентификатор товара.

        Returns:
            ProductWithRelationsRDTO: Объект товара с отношениями.

        Raises:
            AppExceptionResponse: Если товар не найден.
        """
        await self.validate(id=id)
        return ProductWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидирует существование товара с данным ID.

        Args:
            id (int): Идентификатор товара для поиска.

        Raises:
            AppExceptionResponse: Если товар не найден.
        """
        self.model = await self.repository.get(
            id=id,
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
