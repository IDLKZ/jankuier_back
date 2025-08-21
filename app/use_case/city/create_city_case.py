from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.city.city_dto import CityCDTO, CityWithRelationsRDTO
from app.adapters.repository.city.city_repository import CityRepository
from app.adapters.repository.country.country_repository import CountryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CityEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateCityCase(BaseUseCase[CityWithRelationsRDTO]):
    """
    Класс Use Case для создания нового города.

    Использует:
        - Репозиторий `CityRepository` для работы с базой данных.
        - Репозиторий `CountryRepository` для проверки существования страны.
        - DTO `CityCDTO` для входных данных.
        - DTO `CityWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (CityRepository): Репозиторий для работы с городами.
        country_repository (CountryRepository): Репозиторий для работы со странами.
        model (CityEntity | None): Созданная модель города.

    Методы:
        execute(dto: CityCDTO) -> CityWithRelationsRDTO:
            Создает новый город и возвращает DTO.
        validate(dto: CityCDTO):
            Проверяет корректность входных данных.
        transform(dto: CityCDTO):
            Преобразует DTO в модель.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CityRepository(db)
        self.country_repository = CountryRepository(db)
        self.model: CityEntity | None = None

    async def execute(self, dto: CityCDTO) -> CityWithRelationsRDTO:
        """
        Выполняет операцию создания города.

        Args:
            dto (CityCDTO): Данные для создания города.

        Returns:
            CityWithRelationsRDTO: Созданный город с связями.

        Raises:
            AppExceptionResponse: Если страна не найдена.
        """
        await self.validate(dto)
        await self.transform(dto)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return CityWithRelationsRDTO.from_orm(model)

    async def validate(self, dto: CityCDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (CityCDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если страна не найдена.
        """
        # Проверка существования страны
        country = await self.country_repository.get(dto.country_id)
        if not country:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("country_not_found")
            )

    async def transform(self, dto: CityCDTO) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (CityCDTO): Данные для преобразования.
        """
        self.model = CityEntity(**dto.dict())
