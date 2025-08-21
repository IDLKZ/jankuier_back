from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.city.city_dto import CityCDTO, CityWithRelationsRDTO
from app.adapters.repository.city.city_repository import CityRepository
from app.adapters.repository.country.country_repository import CountryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CityEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateCityCase(BaseUseCase[CityWithRelationsRDTO]):
    """
    Класс Use Case для обновления города.

    Использует:
        - Репозиторий `CityRepository` для работы с базой данных.
        - Репозиторий `CountryRepository` для проверки существования страны.
        - DTO `CityCDTO` для входных данных.
        - DTO `CityWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (CityRepository): Репозиторий для работы с городами.
        country_repository (CountryRepository): Репозиторий для работы со странами.
        model (CityEntity | None): Обновляемая модель города.

    Методы:
        execute(id: int, dto: CityCDTO) -> CityWithRelationsRDTO:
            Обновляет город и возвращает DTO.
        validate(id: int, dto: CityCDTO):
            Проверяет существование города и корректность данных.
        transform(dto: CityCDTO):
            Преобразует входные данные.
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

    async def execute(self, id: int, dto: CityCDTO) -> CityWithRelationsRDTO:
        """
        Выполняет операцию обновления города.

        Args:
            id (int): Идентификатор города.
            dto (CityCDTO): Данные для обновления города.

        Returns:
            CityWithRelationsRDTO: Обновленный город с связями.

        Raises:
            AppExceptionResponse: Если город или страна не найдены.
        """
        await self.validate(id=id, dto=dto)
        await self.transform(dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return CityWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int, dto: CityCDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор города для проверки.
            dto (CityCDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если город или страна не найдены.
        """
        # Проверка существования города
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Проверка существования страны
        country = await self.country_repository.get(dto.country_id)
        if not country:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("country_not_found")
            )

    async def transform(self, dto: CityCDTO) -> None:
        """
        Преобразование входных данных.

        Args:
            dto (CityCDTO): Данные для преобразования.
        """
        # Дополнительные преобразования можно добавить здесь при необходимости
        pass