from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.booking_field_party_request.booking_field_party_request_repository import (
    BookingFieldPartyRequestRepository
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class DeleteMyBookingFieldPartyRequestCase(BaseUseCase[bool]):
    """
    Use Case для удаления собственной заявки на бронирование.

    Ограничения:
    - Заявка должна принадлежать текущему пользователю
    - Заявка должна иметь статус "Ожидание оплаты" (status_id = 1)
    - Удаление может быть как мягким (soft delete), так и жестким (force delete)

    Attributes:
        booking_field_party_request_repository: Репозиторий для работы с заявками на бронирование
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db: Асинхронная сессия базы данных
        """
        self.booking_field_party_request_repository = BookingFieldPartyRequestRepository(db)

    async def execute(
        self,
        id: int,
        user: UserWithRelationsRDTO,
        force_delete: bool = False
    ) -> bool:
        """
        Удаляет собственную заявку на бронирование (только со статусом "Ожидание оплаты").

        Args:
            id: ID заявки на бронирование
            user: Текущий авторизованный пользователь
            force_delete: Если True - физическое удаление, иначе - мягкое удаление

        Returns:
            bool: True если заявка успешно удалена

        Raises:
            AppExceptionResponse.not_found: Если заявка не найдена или не принадлежит пользователю
            AppExceptionResponse.bad_request: Если заявка не в статусе "Ожидание оплаты"
        """
        # Проверяем существование заявки и принадлежность пользователю
        booking_request = await self.booking_field_party_request_repository.get_first_with_filters(
            filters=[
                self.booking_field_party_request_repository.model.id == id,
                self.booking_field_party_request_repository.model.user_id == user.id
            ]
        )

        if not booking_request:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("booking_field_party_request_not_found")
            )

        # Проверяем, что заявка в статусе "Ожидание оплаты"
        if booking_request.status_id != DbValueConstants.BookingFieldPartyStatusCreatedAwaitingPaymentID:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("booking_cannot_be_deleted")
            )

        # Удаляем заявку
        return await self.booking_field_party_request_repository.delete(
            id=id,
            force_delete=force_delete
        )

    async def validate(self) -> None:
        """Валидация не требуется для данного use case."""
        pass
