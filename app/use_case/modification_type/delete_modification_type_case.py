from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.modification_type.modification_type_repository import ModificationTypeRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ModificationTypeEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteModificationTypeCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления типа модификации.

    Использует:
        - Репозиторий `ModificationTypeRepository` для работы с базой данных.

    Атрибуты:
        repository (ModificationTypeRepository): Репозиторий для работы с типами модификаций.
        model (ModificationTypeEntity | None): Модель типа модификации для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Выполняет удаление типа модификации.
        validate(id: int):
            Валидирует возможность удаления типа модификации.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ModificationTypeRepository(db)
        self.model: ModificationTypeEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления типа модификации.

        Args:
            id (int): Идентификатор типа модификации.
            force_delete (bool): Флаг принудительного удаления (по умолчанию False - мягкое удаление).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если тип модификации не найден.
        """
        await self.validate(id=id)
        return await self.repository.delete(id=id, force_delete=force_delete)

    async def validate(self, id: int) -> None:
        """
        Валидирует возможность удаления типа модификации.

        Args:
            id (int): Идентификатор типа модификации.

        Raises:
            AppExceptionResponse: Если тип модификации не найден.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))