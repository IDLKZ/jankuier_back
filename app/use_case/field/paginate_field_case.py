from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationFieldWithRelationsRDTO
from app.adapters.dto.field.field_dto import FieldWithRelationsRDTO
from app.adapters.filters.field.field_pagination_filter import FieldPaginationFilter
from app.adapters.repository.field.field_repository import FieldRepository
from app.use_case.base_case import BaseUseCase


class PaginateFieldCase(BaseUseCase[PaginationFieldWithRelationsRDTO]):
    """
    Класс Use Case для получения полей с пагинацией.

    Использует:
        - Репозиторий `FieldRepository` для работы с базой данных.
        - DTO `FieldWithRelationsRDTO` для возврата данных с связями.
        - `PaginationFieldWithRelationsRDTO` для пагинированного ответа.

    Атрибуты:
        repository (FieldRepository): Репозиторий для работы с полями.

    Методы:
        execute() -> PaginationFieldWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список полей.
        validate():
            Метод валидации (пока пустой).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldRepository(db)

    async def execute(self, filter: FieldPaginationFilter) -> PaginationFieldWithRelationsRDTO:
        """
        Выполняет операцию получения полей с пагинацией.

        Args:
            filter (FieldPaginationFilter): Фильтр с параметрами пагинации.

        Returns:
            PaginationFieldWithRelationsRDTO: Пагинированный список полей с связями.
        """
        models = await self.repository.paginate(
            dto=FieldWithRelationsRDTO,
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