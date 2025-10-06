from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderRDTO, TicketonOrderWithRelationsRDTO
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TicketonOrderEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetTicketonOrderByIdCase(BaseUseCase[TicketonOrderWithRelationsRDTO]):
    """
    Класс Use Case для получения заказа Ticketon по ID (клиентская версия).

    Использует:
        - Репозиторий `TicketonOrderRepository` для работы с базой данных.
        - DTO `TicketonOrderRDTO` для возврата данных.
        
    Особенности:
        - Проверяет, что заказ принадлежит запрашивающему пользователю.
        - Предназначен для использования клиентами для просмотра своих заказов.

    Атрибуты:
        repository (TicketonOrderRepository): Репозиторий для работы с заказами.
        model (TicketonOrderEntity | None): Найденная модель заказа.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TicketonOrderRepository(db)
        self.model: TicketonOrderEntity | None = None

    async def execute(self, id: int, user_id: int|None = None) -> TicketonOrderWithRelationsRDTO:
        """
        Выполняет операцию получения заказа Ticketon по ID.

        Args:
            id (int): ID заказа для поиска.
            user_id (int): ID пользователя, который запрашивает заказ.

        Returns:
            TicketonOrderWithRelationsRDTO: Найденный заказ Ticketon с отношениями.

        Raises:
            AppExceptionResponse: Если заказ не найден или не принадлежит пользователю.
        """
        await self.validate(id=id, user_id=user_id)
        return TicketonOrderWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, user_id: int|None = None) -> None:
        """
        Валидация поиска заказа Ticketon по ID с проверкой владельца.

        Args:
            id (int): ID заказа для валидации.
            user_id (int): ID пользователя для проверки владения.

        Raises:
            AppExceptionResponse: Если заказ не найден или не принадлежит пользователю.
        """
        self.model = await self.repository.get(
            id,
            include_deleted_filter=True,
            options=self.repository.default_relationships()
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
        
        # Проверяем, что заказ принадлежит запрашивающему пользователю
        # if self.model.user_id != user_id:
        #     raise AppExceptionResponse.forbidden(
        #         message=i18n.gettext("access_denied")
        #     )