from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.role.role_dto import RoleRDTO
from app.adapters.filters.role.role_filter import RoleFilter
from app.adapters.repository.role.role_repository import RoleRepository
from app.use_case.base_case import BaseUseCase


class AllRoleCase(BaseUseCase[list[RoleRDTO]]):
    """
    Класс Use Case для получения списка всех ролей.

    Использует:
        - Репозиторий `RoleRepository` для работы с базой данных.
        - DTO `RoleRDTO` для возврата данных.

    Атрибуты:
        repository (RoleRepository): Репозиторий для работы с ролями.

    Методы:
        execute() -> list[RoleRDTO]:
            Выполняет запрос и возвращает список всех ролей.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = RoleRepository(db)

    async def execute(self, filter: RoleFilter) -> list[RoleRDTO]:
        """
        Выполняет операцию получения списка всех ролей.

        Returns:
            list[RoleRDTO]: Список объектов ролей.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [RoleRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
