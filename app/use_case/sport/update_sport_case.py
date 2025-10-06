from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.sport.sport_dto import SportCDTO, SportRDTO
from app.adapters.repository.sport.sport_repository import SportRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import SportEntity
from app.i18n.i18n_wrapper import i18n
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class UpdateSportCase(BaseUseCase[SportRDTO]):
    """
    Класс Use Case для обновления вида спорта.

    Использует:
        - Репозиторий `SportRepository` для работы с базой данных.
        - DTO `SportCDTO` для входных данных.
        - DTO `SportRDTO` для возврата данных.

    Атрибуты:
        repository (SportRepository): Репозиторий для работы с видами спорта.
        model (SportEntity | None): Модель вида спорта для обновления.

    Методы:
        execute(id: int, dto: SportCDTO) -> SportRDTO:
            Выполняет обновление вида спорта.
        validate(id: int, dto: SportCDTO):
            Валидирует данные перед обновлением.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = SportRepository(db)
        self.model: SportEntity | None = None

    async def execute(self, id: int, dto: SportCDTO) -> SportRDTO:
        """
        Выполняет операцию обновления вида спорта.

        Args:
            id (int): Идентификатор вида спорта.
            dto (SportCDTO): DTO с данными для обновления.

        Returns:
            SportRDTO: Обновленный объект вида спорта.

        Raises:
            AppExceptionResponse: Если вид спорта не найден или значение уже существует.
        """
        await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        return SportRDTO.from_orm(model)

    async def validate(self, id: int, dto: SportCDTO) -> None:
        """
        Валидирует данные перед обновлением вида спорта.

        Args:
            id (int): Идентификатор вида спорта.
            dto (SportCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если вид спорта не найден или значение уже существует.
        """
        # Проверка существования вида спорта
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))

        # Автогенерация value из title_ru если не предоставлено
        if dto.value is None:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Проверка уникальности значения (исключая текущую запись)
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id != id,
                    self.repository.model.value == dto.value,
                )
            ],
            include_deleted_filter=True,
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
            )
