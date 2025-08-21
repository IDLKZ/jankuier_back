from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.sport.sport_dto import SportCDTO, SportRDTO
from app.adapters.repository.sport.sport_repository import SportRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import SportEntity
from app.i18n.i18n_wrapper import i18n
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CreateSportCase(BaseUseCase[SportRDTO]):
    """
    Класс Use Case для создания нового вида спорта.

    Использует:
        - Репозиторий `SportRepository` для работы с базой данных.
        - DTO `SportCDTO` для входных данных.
        - DTO `SportRDTO` для возврата данных.

    Атрибуты:
        repository (SportRepository): Репозиторий для работы с видами спорта.
        model (SportEntity | None): Модель вида спорта для создания.

    Методы:
        execute(dto: SportCDTO) -> SportRDTO:
            Выполняет создание вида спорта.
        validate(dto: SportCDTO):
            Валидирует данные перед созданием.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = SportRepository(db)
        self.model: SportEntity | None = None

    async def execute(self, dto: SportCDTO) -> SportRDTO:
        """
        Выполняет операцию создания нового вида спорта.

        Args:
            dto (SportCDTO): DTO с данными для создания вида спорта.

        Returns:
            SportRDTO: Созданный объект вида спорта.

        Raises:
            AppExceptionResponse: Если вид спорта с таким значением уже существует.
        """
        await self.validate(dto)
        model = await self.repository.create(self.model)
        return SportRDTO.from_orm(model)

    async def validate(self, dto: SportCDTO) -> None:
        """
        Валидирует данные перед созданием вида спорта.

        Args:
            dto (SportCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если вид спорта с таким значением уже существует.
        """
        # Автогенерация value из title_ru если не предоставлено
        if dto.value is None:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Проверка уникальности значения
        existed = await self.repository.get_first_with_filters(
            filters=[self.repository.model.value == dto.value]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
            )

        # Создание модели для сохранения
        self.model = SportEntity(**dto.dict())