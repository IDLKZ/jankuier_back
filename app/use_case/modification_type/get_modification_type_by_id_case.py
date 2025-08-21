from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.modification_type.modification_type_dto import (
    ModificationTypeRDTO,
)
from app.adapters.repository.modification_type.modification_type_repository import (
    ModificationTypeRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ModificationTypeEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetModificationTypeByIdCase(BaseUseCase[ModificationTypeRDTO]):
    """
    Класс Use Case для получения типа модификации по ID.

    Использует:
        - Репозиторий `ModificationTypeRepository` для работы с базой данных.
        - DTO `ModificationTypeRDTO` для возврата данных.

    Атрибуты:
        repository (ModificationTypeRepository): Репозиторий для работы с типами модификаций.
        model (ModificationTypeEntity | None): Найденная модель типа модификации.

    Методы:
        execute(id: int) -> ModificationTypeRDTO:
            Выполняет поиск и возвращает тип модификации по ID.
        validate(id: int):
            Валидирует существование типа модификации с данным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ModificationTypeRepository(db)
        self.model: ModificationTypeEntity | None = None

    async def execute(self, id: int) -> ModificationTypeRDTO:
        """
        Выполняет операцию получения типа модификации по ID.

        Args:
            id (int): Идентификатор типа модификации.

        Returns:
            ModificationTypeRDTO: Объект типа модификации.

        Raises:
            AppExceptionResponse: Если тип модификации не найден.
        """
        await self.validate(id=id)
        return ModificationTypeRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидирует существование типа модификации с данным ID.

        Args:
            id (int): Идентификатор типа модификации для поиска.

        Raises:
            AppExceptionResponse: Если тип модификации не найден.
        """
        self.model = await self.repository.get(
            id=id,
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
