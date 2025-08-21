from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.country.country_dto import CountryCDTO, CountryRDTO
from app.adapters.repository.country.country_repository import CountryRepository
from app.entities import CountryEntity
from app.use_case.base_case import BaseUseCase


class CreateCountryCase(BaseUseCase[CountryRDTO]):
    """
    Класс Use Case для создания новой страны.

    Использует:
        - Репозиторий `CountryRepository` для работы с базой данных.
        - DTO `CountryCDTO` для входных данных.
        - DTO `CountryRDTO` для возврата данных.

    Атрибуты:
        repository (CountryRepository): Репозиторий для работы со странами.
        model (CountryEntity | None): Созданная модель страны.

    Методы:
        execute(dto: CountryCDTO) -> CountryRDTO:
            Создает новую страну и возвращает DTO.
        validate(dto: CountryCDTO):
            Проверяет корректность входных данных.
        transform(dto: CountryCDTO):
            Преобразует DTO в модель.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CountryRepository(db)
        self.model: CountryEntity | None = None

    async def execute(self, dto: CountryCDTO) -> CountryRDTO:
        """
        Выполняет операцию создания страны.

        Args:
            dto (CountryCDTO): Данные для создания страны.

        Returns:
            CountryRDTO: Созданная страна.
        """
        await self.validate(dto)
        await self.transform(dto)
        model = await self.repository.create(self.model)
        return CountryRDTO.from_orm(model)

    async def validate(self, dto: CountryCDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (CountryCDTO): Данные для валидации.
        """
        # Дополнительные проверки можно добавить здесь при необходимости
        pass

    async def transform(self, dto: CountryCDTO) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (CountryCDTO): Данные для преобразования.
        """
        self.model = CountryEntity(**dto.dict())
