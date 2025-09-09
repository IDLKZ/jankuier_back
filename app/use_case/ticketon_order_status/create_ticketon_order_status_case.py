from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.ticketon_order_status.ticketon_order_status_dto import TicketonOrderStatusCDTO, TicketonOrderStatusRDTO
from app.adapters.repository.ticketon_order_status.ticketon_order_status_repository import TicketonOrderStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TicketonOrderStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateTicketonOrderStatusCase(BaseUseCase[TicketonOrderStatusRDTO]):
    """
    Класс Use Case для создания статуса заказа Ticketon.

    Использует:
        - Репозиторий `TicketonOrderStatusRepository` для работы с базой данных.
        - DTO `TicketonOrderStatusCDTO` для входных данных.
        - DTO `TicketonOrderStatusRDTO` для возврата данных.

    Атрибуты:
        repository (TicketonOrderStatusRepository): Репозиторий для работы со статусами.
        model (TicketonOrderStatusEntity | None): Модель статуса для создания.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TicketonOrderStatusRepository(db)
        self.model: TicketonOrderStatusEntity | None = None

    async def execute(self, dto: TicketonOrderStatusCDTO) -> TicketonOrderStatusRDTO:
        """
        Выполняет операцию создания статуса заказа Ticketon.

        Args:
            dto (TicketonOrderStatusCDTO): DTO с данными для создания статуса.

        Returns:
            TicketonOrderStatusRDTO: Созданный статус заказа Ticketon.
        """
        await self.validate(dto)
        model = await self.repository.create(self.model)
        return TicketonOrderStatusRDTO.from_orm(model)

    async def validate(self, dto: TicketonOrderStatusCDTO) -> None:
        """
        Валидация данных для создания статуса заказа Ticketon.

        Args:
            dto (TicketonOrderStatusCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если статус с таким названием уже существует.
        """
        # Проверяем уникальность названия статуса
        existed = await self.repository.get_first_with_filters(
            filters=[self.repository.model.title_ru == dto.title_ru]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.title_ru}"
            )
        
        self.model = TicketonOrderStatusEntity(**dto.dict())