from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.sport.sport_dto import SportRDTO
from app.adapters.repository.sport.sport_repository import SportRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import SportEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetSportByIdCase(BaseUseCase[SportRDTO]):
    """
    Класс Use Case для получения вида спорта по ID.

    Использует:
        - Репозиторий `SportRepository` для работы с базой данных.
        - DTO `SportRDTO` для возврата данных.

    Атрибуты:
        repository (SportRepository): Репозиторий для работы с видами спорта.
        model (SportEntity | None): Найденная модель вида спорта.

    Методы:
        execute(id: int) -> SportRDTO:
            Выполняет поиск и возвращает вид спорта по ID.
        validate(id: int):
            Валидирует существование вида спорта с данным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = SportRepository(db)
        self.model: SportEntity | None = None

    async def execute(self, id: int) -> SportRDTO:
        """
        Выполняет операцию получения вида спорта по ID.

        Args:
            id (int): Идентификатор вида спорта.

        Returns:
            SportRDTO: Объект вида спорта.

        Raises:
            AppExceptionResponse: Если вид спорта не найден.
        """
        await self.validate(id=id)
        return SportRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидирует существование вида спорта с данным ID.

        Args:
            id (int): Идентификатор вида спорта для поиска.

        Raises:
            AppExceptionResponse: Если вид спорта не найден.
        """
        self.model = await self.repository.get(
            id=id,
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))