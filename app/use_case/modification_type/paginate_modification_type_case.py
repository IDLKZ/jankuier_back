from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationModificationTypeRDTO
from app.adapters.dto.modification_type.modification_type_dto import (
    ModificationTypeRDTO,
)
from app.adapters.filters.modification_type.modification_type_pagination_filter import (
    ModificationTypePaginationFilter,
)
from app.adapters.repository.modification_type.modification_type_repository import (
    ModificationTypeRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateModificationTypeCase(BaseUseCase[PaginationModificationTypeRDTO]):
    """
    Класс Use Case для получения пагинированного списка типов модификаций.

    Использует:
        - Репозиторий `ModificationTypeRepository` для работы с базой данных.
        - DTO `ModificationTypeRDTO` для возврата данных.
        - Фильтр `ModificationTypePaginationFilter` для пагинации и фильтрации.

    Атрибуты:
        repository (ModificationTypeRepository): Репозиторий для работы с типами модификаций.

    Методы:
        execute(filter: ModificationTypePaginationFilter) -> PaginationModificationTypeRDTO:
            Выполняет запрос и возвращает пагинированный список типов модификаций.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ModificationTypeRepository(db)

    async def execute(
        self, filter: ModificationTypePaginationFilter
    ) -> PaginationModificationTypeRDTO:
        """
        Выполняет операцию получения пагинированного списка типов модификаций.

        Args:
            filter (ModificationTypePaginationFilter): Фильтр пагинации с параметрами поиска и сортировки.

        Returns:
            PaginationModificationTypeRDTO: Объект пагинации с типами модификаций.
        """
        pagination = await self.repository.paginate(
            dto=ModificationTypeRDTO,
            page=filter.page,
            per_page=filter.per_page,
            filters=filter.apply(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return pagination

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
