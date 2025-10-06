from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.product_variant_modification.product_variant_modification_repository import (
    ProductVariantModificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductVariantModificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteProductVariantModificationCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления модификации варианта товара.

    Использует:
        - Репозиторий `ProductVariantModificationRepository` для работы с базой данных.

    Атрибуты:
        repository (ProductVariantModificationRepository): Репозиторий для работы с модификациями вариантов товаров.
        model (ProductVariantModificationEntity | None): Модель модификации варианта товара для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Выполняет удаление модификации варианта товара.
        validate(id: int):
            Валидирует возможность удаления модификации варианта товара.
        transform(force_delete: bool = False):
            Трансформирует операцию удаления.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductVariantModificationRepository(db)
        self.model: ProductVariantModificationEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления модификации варианта товара.

        Args:
            id (int): Идентификатор модификации варианта товара для удаления.
            force_delete (bool): Флаг принудительного удаления (полное удаление из БД).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если модификация варианта товара не найдена или удаление невозможно.
        """
        await self.validate(id=id)
        await self.transform(force_delete=force_delete)
        return True

    async def validate(self, id: int) -> None:
        """
        Валидирует возможность удаления модификации варианта товара.

        Args:
            id (int): Идентификатор модификации варианта товара для удаления.

        Raises:
            AppExceptionResponse: Если модификация варианта товара не найдена.
        """
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))

    async def transform(self, force_delete: bool = False):
        """
        Трансформирует операцию удаления модификации варианта товара.

        Args:
            force_delete (bool): Флаг принудительного удаления.
        """
        # Выполнение удаления
        await self.repository.delete(id=self.model.id, force_delete=force_delete)
