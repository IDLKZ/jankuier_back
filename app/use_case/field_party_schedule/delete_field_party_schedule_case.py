from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.field_party_schedule.field_party_schedule_repository import (
    FieldPartyScheduleRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldPartyScheduleEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteFieldPartyScheduleCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления расписания площадки.

    Использует:
        - Репозиторий `FieldPartyScheduleRepository` для работы с базой данных.

    Атрибуты:
        repository (FieldPartyScheduleRepository): Репозиторий для работы с расписаниями.
        model (FieldPartyScheduleEntity | None): Удаляемая модель расписания.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyScheduleRepository(db)
        self.model: FieldPartyScheduleEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления расписания площадки.

        Args:
            id (int): Идентификатор расписания площадки для удаления.
            force_delete (bool): Принудительное удаление (по умолчанию False - мягкое удаление).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, force_delete=force_delete)

        result = await self.repository.delete(id, force_delete=force_delete)
        return result

    async def validate(self, id: int, force_delete: bool = False) -> None:
        """
        Валидация перед выполнением удаления.

        Args:
            id (int): Идентификатор расписания площадки для валидации.
            force_delete (bool): Принудительное удаление.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка валидности ID
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("schedule_id_validation_error")
            )

        # Проверка существования расписания
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("field_party_schedule_not_found")
            )

        # Бизнес-правила для удаления
        if not force_delete:
            # Нельзя удалить забронированное расписание
            if model.is_booked:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("schedule_already_booked_error")
                )

            # Нельзя удалить оплаченное расписание
            if model.is_paid:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("schedule_already_paid_error")
                )

        self.model = model
