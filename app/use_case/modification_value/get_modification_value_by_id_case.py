from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.modification_value.modification_value_dto import ModificationValueWithRelationsRDTO
from app.adapters.repository.modification_value.modification_value_repository import ModificationValueRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ModificationValueEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetModificationValueByIdCase(BaseUseCase[ModificationValueWithRelationsRDTO]):
    """
    Класс Use Case для получения значения модификации по ID.

    Использует:
        - Репозиторий `ModificationValueRepository` для работы с базой данных.
        - DTO `ModificationValueWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ModificationValueRepository): Репозиторий для работы со значениями модификаций.
        model (ModificationValueEntity | None): Найденная модель значения модификации.

    Методы:
        execute(id: int) -> ModificationValueWithRelationsRDTO:
            Выполняет поиск и возвращает значение модификации по ID.
        validate(id: int):
            Валидирует существование значения модификации с данным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ModificationValueRepository(db)
        self.model: ModificationValueEntity | None = None

    async def execute(self, id: int) -> ModificationValueWithRelationsRDTO:
        """
        Выполняет операцию получения значения модификации по ID.

        Args:
            id (int): Идентификатор значения модификации.

        Returns:
            ModificationValueWithRelationsRDTO: Объект значения модификации с отношениями.

        Raises:
            AppExceptionResponse: Если значение модификации не найдено.
        """
        await self.validate(id=id)
        return ModificationValueWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидирует существование значения модификации с данным ID.

        Args:
            id (int): Идентификатор значения модификации для поиска.

        Raises:
            AppExceptionResponse: Если значение модификации не найдено.
        """
        self.model = await self.repository.get(
            id=id,
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))