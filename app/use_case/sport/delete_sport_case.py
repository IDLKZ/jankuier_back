from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.sport.sport_repository import SportRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import SportEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteSportCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления вида спорта.

    Использует:
        - Репозиторий `SportRepository` для работы с базой данных.

    Атрибуты:
        repository (SportRepository): Репозиторий для работы с видами спорта.
        model (SportEntity | None): Модель вида спорта для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Выполняет удаление вида спорта.
        validate(id: int):
            Валидирует возможность удаления вида спорта.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = SportRepository(db)
        self.model: SportEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления вида спорта.

        Args:
            id (int): Идентификатор вида спорта.
            force_delete (bool): Флаг принудительного удаления (по умолчанию False - мягкое удаление).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если вид спорта не найден.
        """
        await self.validate(id=id)
        return await self.repository.delete(id=id, force_delete=force_delete)

    async def validate(self, id: int) -> None:
        """
        Валидирует возможность удаления вида спорта.

        Args:
            id (int): Идентификатор вида спорта.

        Raises:
            AppExceptionResponse: Если вид спорта не найден.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
