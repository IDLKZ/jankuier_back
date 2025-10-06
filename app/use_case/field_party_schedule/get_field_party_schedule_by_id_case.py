from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party_schedule.field_party_schedule_dto import (
    FieldPartyScheduleRDTO,
)
from app.adapters.repository.field_party_schedule.field_party_schedule_repository import (
    FieldPartyScheduleRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetFieldPartyScheduleByIdCase(BaseUseCase[FieldPartyScheduleRDTO]):
    """
    Класс Use Case для получения расписания площадки по ID.

    Использует:
        - Репозиторий `FieldPartyScheduleRepository` для работы с базой данных.
        - DTO `FieldPartyScheduleRDTO` для возврата данных.

    Атрибуты:
        repository (FieldPartyScheduleRepository): Репозиторий для работы с расписаниями площадок.

    Методы:
        execute() -> FieldPartyScheduleRDTO:
            Выполняет запрос и возвращает расписание площадки по ID.
        validate():
            Валидация входных данных.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyScheduleRepository(db)

    async def execute(self, id: int) -> FieldPartyScheduleRDTO:
        """
        Выполняет операцию получения расписания площадки по ID.

        Args:
            id (int): ID расписания площадки.

        Returns:
            FieldPartyScheduleRDTO: Объект расписания площадки.

        Raises:
            AppExceptionResponse: Если расписание площадки не найдено.
        """
        await self.validate(id)

        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("field_party_schedule_not_found")
            )

        return FieldPartyScheduleRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        """
        Валидация входных данных.

        Args:
            id (int): ID расписания площадки для валидации.

        Raises:
            AppExceptionResponse: Если ID недействителен.
        """
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("schedule_id_validation_error")
            )
