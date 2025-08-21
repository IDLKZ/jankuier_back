from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationFieldPartyWithRelationsRDTO
from app.adapters.dto.field_party.field_party_dto import FieldPartyWithRelationsRDTO
from app.adapters.filters.field_party.field_party_pagination_filter import (
    FieldPartyPaginationFilter,
)
from app.adapters.repository.field_party.field_party_repository import (
    FieldPartyRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateFieldPartyCase(BaseUseCase[PaginationFieldPartyWithRelationsRDTO]):
    """
    Класс Use Case для получения площадок полей с пагинацией.

    Использует:
        - Репозиторий `FieldPartyRepository` для работы с базой данных.
        - DTO `FieldPartyWithRelationsRDTO` для возврата данных с связями.
        - `PaginationFieldPartyWithRelationsRDTO` для пагинированного ответа.

    Атрибуты:
        repository (FieldPartyRepository): Репозиторий для работы с площадками полей.

    Методы:
        execute() -> PaginationFieldPartyWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список площадок полей.
        validate():
            Метод валидации (пока пустой).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyRepository(db)

    async def execute(
        self, filter: FieldPartyPaginationFilter
    ) -> PaginationFieldPartyWithRelationsRDTO:
        """
        Выполняет операцию получения площадок полей с пагинацией.

        Args:
            filter (FieldPartyPaginationFilter): Фильтр с параметрами пагинации.

        Returns:
            PaginationFieldPartyWithRelationsRDTO: Пагинированный список площадок полей с связями.
        """
        models = await self.repository.paginate(
            dto=FieldPartyWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return models

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
