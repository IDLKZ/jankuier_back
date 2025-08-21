from sqlalchemy import func
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


class GetModificationTypeByValueCase(BaseUseCase[ModificationTypeRDTO]):
    """
    Класс Use Case для получения типа модификации по уникальному значению.

    Использует:
        - Репозиторий `ModificationTypeRepository` для работы с базой данных.
        - DTO `ModificationTypeRDTO` для возврата данных.

    Атрибуты:
        repository (ModificationTypeRepository): Репозиторий для работы с типами модификаций.
        model (ModificationTypeEntity | None): Найденная модель типа модификации.

    Методы:
        execute(value: str) -> ModificationTypeRDTO:
            Выполняет поиск и возвращает тип модификации по уникальному значению.
        validate(value: str):
            Валидирует существование типа модификации с данным значением.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ModificationTypeRepository(db)
        self.model: ModificationTypeEntity | None = None

    async def execute(self, value: str) -> ModificationTypeRDTO:
        """
        Выполняет операцию получения типа модификации по уникальному значению.

        Args:
            value (str): Уникальное значение типа модификации.

        Returns:
            ModificationTypeRDTO: Объект типа модификации.

        Raises:
            AppExceptionResponse: Если тип модификации не найден.
        """
        await self.validate(value=value)
        return ModificationTypeRDTO.from_orm(self.model)

    async def validate(self, value: str) -> None:
        """
        Валидирует существование типа модификации с данным значением.

        Args:
            value (str): Уникальное значение типа модификации для поиска.

        Raises:
            AppExceptionResponse: Если тип модификации не найден.
        """
        self.model = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == value.lower()],
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
