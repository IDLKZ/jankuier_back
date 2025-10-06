from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.country.country_dto import CountryRDTO
from app.adapters.repository.country.country_repository import CountryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CountryEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetCountryByIdCase(BaseUseCase[CountryRDTO]):
    """
    Класс Use Case для получения страны по ID.

    Использует:
        - Репозиторий `CountryRepository` для работы с базой данных.
        - DTO `CountryRDTO` для возврата данных.

    Атрибуты:
        repository (CountryRepository): Репозиторий для работы со странами.
        model (CountryEntity | None): Найденная модель страны.

    Методы:
        execute(id: int) -> CountryRDTO:
            Выполняет поиск страны по ID и возвращает DTO.
        validate(id: int):
            Проверяет существование страны с указанным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CountryRepository(db)
        self.model: CountryEntity | None = None

    async def execute(self, id: int) -> CountryRDTO:
        """
        Выполняет операцию получения страны по ID.

        Args:
            id (int): Идентификатор страны.

        Returns:
            CountryRDTO: Объект страны.

        Raises:
            AppExceptionResponse: Если страна не найдена.
        """
        await self.validate(id=id)
        return CountryRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор страны для проверки.

        Raises:
            AppExceptionResponse: Если страна не найдена.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
