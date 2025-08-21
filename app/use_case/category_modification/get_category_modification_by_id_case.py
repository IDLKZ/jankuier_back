from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.category_modification.category_modification_dto import (
    CategoryModificationWithRelationsRDTO,
)
from app.adapters.repository.category_modification.category_modification_repository import (
    CategoryModificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CategoryModificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetCategoryModificationByIdCase(
    BaseUseCase[CategoryModificationWithRelationsRDTO]
):
    """
    Класс Use Case для получения модификации категории по ID.

    Использует:
        - Репозиторий `CategoryModificationRepository` для работы с базой данных.
        - DTO `CategoryModificationWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (CategoryModificationRepository): Репозиторий для работы с модификациями категорий.
        model (CategoryModificationEntity | None): Найденная модель модификации категории.

    Методы:
        execute(id: int) -> CategoryModificationWithRelationsRDTO:
            Выполняет поиск и возвращает модификацию категории по ID.
        validate(id: int):
            Валидирует существование модификации категории с данным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CategoryModificationRepository(db)
        self.model: CategoryModificationEntity | None = None

    async def execute(self, id: int) -> CategoryModificationWithRelationsRDTO:
        """
        Выполняет операцию получения модификации категории по ID.

        Args:
            id (int): Идентификатор модификации категории.

        Returns:
            CategoryModificationWithRelationsRDTO: Объект модификации категории с отношениями.

        Raises:
            AppExceptionResponse: Если модификация категории не найдена.
        """
        await self.validate(id=id)
        return CategoryModificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидирует существование модификации категории с данным ID.

        Args:
            id (int): Идентификатор модификации категории для поиска.

        Raises:
            AppExceptionResponse: Если модификация категории не найдена.
        """
        self.model = await self.repository.get(
            id=id,
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
