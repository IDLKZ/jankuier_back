from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.modification_value.modification_value_repository import (
    ModificationValueRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ModificationValueEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteModificationValueCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления значения модификации.

    Использует:
        - Репозиторий `ModificationValueRepository` для работы с базой данных.

    Атрибуты:
        repository (ModificationValueRepository): Репозиторий для работы со значениями модификаций.
        model (ModificationValueEntity | None): Модель значения модификации для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Выполняет удаление значения модификации.
        validate(id: int):
            Валидирует возможность удаления значения модификации.
        transform(force_delete: bool = False):
            Трансформирует операцию удаления.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ModificationValueRepository(db)
        self.model: ModificationValueEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления значения модификации.

        Args:
            id (int): Идентификатор значения модификации для удаления.
            force_delete (bool): Флаг принудительного удаления (полное удаление из БД).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если значение модификации не найдено или удаление невозможно.
        """
        await self.validate(id=id)
        await self.transform(force_delete=force_delete)
        return True

    async def validate(self, id: int) -> None:
        """
        Валидирует возможность удаления значения модификации.

        Args:
            id (int): Идентификатор значения модификации для удаления.

        Raises:
            AppExceptionResponse: Если значение модификации не найдено.
        """
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

    async def transform(self, force_delete: bool = False):
        """
        Трансформирует операцию удаления значения модификации.

        Args:
            force_delete (bool): Флаг принудительного удаления.
        """
        # Выполнение удаления
        await self.repository.delete(id=self.model.id, force_delete=force_delete)
