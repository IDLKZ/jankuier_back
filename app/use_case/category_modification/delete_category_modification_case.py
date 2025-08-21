from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.category_modification.category_modification_repository import CategoryModificationRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CategoryModificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteCategoryModificationCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления модификации категории.

    Использует:
        - Репозиторий `CategoryModificationRepository` для работы с базой данных.

    Атрибуты:
        repository (CategoryModificationRepository): Репозиторий для работы с модификациями категорий.
        model (CategoryModificationEntity | None): Модель модификации категории для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Выполняет удаление модификации категории.
        validate(id: int):
            Валидирует возможность удаления модификации категории.
        transform(force_delete: bool = False):
            Трансформирует операцию удаления.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CategoryModificationRepository(db)
        self.model: CategoryModificationEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления модификации категории.

        Args:
            id (int): Идентификатор модификации категории для удаления.
            force_delete (bool): Флаг принудительного удаления (полное удаление из БД).
                                 Примечание: CategoryModification не поддерживает soft delete (нет поля deleted_at).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если модификация категории не найдена или удаление невозможно.
        """
        await self.validate(id=id)
        await self.transform(force_delete=force_delete)
        return True

    async def validate(self, id: int) -> None:
        """
        Валидирует возможность удаления модификации категории.

        Args:
            id (int): Идентификатор модификации категории для удаления.

        Raises:
            AppExceptionResponse: Если модификация категории не найдена.
        """
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

    async def transform(self, force_delete: bool = False):
        """
        Трансформирует операцию удаления модификации категории.

        Args:
            force_delete (bool): Флаг принудительного удаления.
                                Примечание: CategoryModification всегда удаляется полностью (нет поля deleted_at).
        """
        # Выполнение удаления (всегда force_delete=True, так как нет поля deleted_at)
        await self.repository.delete(id=self.model.id, force_delete=True)