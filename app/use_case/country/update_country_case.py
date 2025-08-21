from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.country.country_dto import CountryCDTO, CountryRDTO
from app.adapters.repository.country.country_repository import CountryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CountryEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateCountryCase(BaseUseCase[CountryRDTO]):
    """
    Класс Use Case для обновления страны.

    Использует:
        - Репозиторий `CountryRepository` для работы с базой данных.
        - DTO `CountryCDTO` для входных данных.
        - DTO `CountryRDTO` для возврата данных.

    Атрибуты:
        repository (CountryRepository): Репозиторий для работы со странами.
        model (CountryEntity | None): Обновляемая модель страны.

    Методы:
        execute(id: int, dto: CountryCDTO) -> CountryRDTO:
            Обновляет страну и возвращает DTO.
        validate(id: int, dto: CountryCDTO):
            Проверяет существование страны и корректность данных.
        transform(dto: CountryCDTO):
            Преобразует входные данные.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CountryRepository(db)
        self.model: CountryEntity | None = None

    async def execute(self, id: int, dto: CountryCDTO) -> CountryRDTO:
        """
        Выполняет операцию обновления страны.

        Args:
            id (int): Идентификатор страны.
            dto (CountryCDTO): Данные для обновления страны.

        Returns:
            CountryRDTO: Обновленная страна.

        Raises:
            AppExceptionResponse: Если страна не найдена.
        """
        await self.validate(id=id, dto=dto)
        await self.transform(dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        return CountryRDTO.from_orm(model)

    async def validate(self, id: int, dto: CountryCDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор страны для проверки.
            dto (CountryCDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если страна не найдена.
        """
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

    async def transform(self, dto: CountryCDTO) -> None:
        """
        Преобразование входных данных.

        Args:
            dto (CountryCDTO): Данные для преобразования.
        """
        # Дополнительные преобразования можно добавить здесь при необходимости
        pass
