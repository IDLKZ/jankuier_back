from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.ticketon_order_status.ticketon_order_status_dto import TicketonOrderStatusRDTO, TicketonOrderStatusCDTO
from app.adapters.repository.ticketon_order_status.ticketon_order_status_repository import TicketonOrderStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TicketonOrderStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateTicketonOrderStatusCase(BaseUseCase[TicketonOrderStatusRDTO]):
    """
    Класс Use Case для обновления статуса заказа Ticketon.

    Использует:
        - Репозиторий `TicketonOrderStatusRepository` для работы с базой данных.
        - DTO `TicketonOrderStatusCDTO` для входных данных.
        - DTO `TicketonOrderStatusRDTO` для возврата данных.

    Атрибуты:
        repository (TicketonOrderStatusRepository): Репозиторий для работы со статусами.
        model (TicketonOrderStatusEntity | None): Модель статуса для обновления.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TicketonOrderStatusRepository(db)
        self.model: TicketonOrderStatusEntity | None = None

    async def execute(self, id: int, dto: TicketonOrderStatusCDTO) -> TicketonOrderStatusRDTO:
        """
        Выполняет операцию обновления статуса заказа Ticketon.

        Args:
            id (int): ID статуса для обновления.
            dto (TicketonOrderStatusCDTO): DTO с обновленными данными.

        Returns:
            TicketonOrderStatusRDTO: Обновленный статус заказа Ticketon.
        """
        await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        return TicketonOrderStatusRDTO.from_orm(model)

    async def validate(self, id: int, dto: TicketonOrderStatusCDTO) -> None:
        """
        Валидация данных для обновления статуса заказа Ticketon.

        Args:
            id (int): ID статуса для валидации.
            dto (TicketonOrderStatusCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если статус не найден или название уже используется.
        """
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
        
        # Проверяем уникальность названия статуса (исключая текущий статус)
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id != id,
                    self.repository.model.title_ru == dto.title_ru,
                )
            ],
            include_deleted_filter=True,
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.title_ru}"
            )