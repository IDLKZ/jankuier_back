from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.city.city_dto import CityWithRelationsRDTO
from app.adapters.repository.city.city_repository import CityRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CityEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetCityByIdCase(BaseUseCase[CityWithRelationsRDTO]):
    """
    Класс Use Case для получения города по ID.

    Использует:
        - Репозиторий `CityRepository` для работы с базой данных.
        - DTO `CityWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (CityRepository): Репозиторий для работы с городами.
        model (CityEntity | None): Найденная модель города.

    Методы:
        execute(id: int) -> CityWithRelationsRDTO:
            Выполняет поиск города по ID и возвращает DTO.
        validate(id: int):
            Проверяет существование города с указанным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CityRepository(db)
        self.model: CityEntity | None = None

    async def execute(self, id: int) -> CityWithRelationsRDTO:
        """
        Выполняет операцию получения города по ID.

        Args:
            id (int): Идентификатор города.

        Returns:
            CityWithRelationsRDTO: Объект города с связями.

        Raises:
            AppExceptionResponse: Если город не найден.
        """
        await self.validate(id=id)
        return CityWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор города для проверки.

        Raises:
            AppExceptionResponse: Если город не найден.
        """
        self.model = await self.repository.get(
            id, 
            options=self.repository.default_relationships(),
            include_deleted_filter=True
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))