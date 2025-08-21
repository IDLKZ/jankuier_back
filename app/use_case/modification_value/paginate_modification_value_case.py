from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationModificationValueWithRelationsRDTO
from app.adapters.dto.modification_value.modification_value_dto import ModificationValueWithRelationsRDTO
from app.adapters.filters.modification_value.modification_value_pagination_filter import ModificationValuePaginationFilter
from app.adapters.repository.modification_value.modification_value_repository import ModificationValueRepository
from app.use_case.base_case import BaseUseCase


class PaginateModificationValueCase(BaseUseCase[PaginationModificationValueWithRelationsRDTO]):
    """
    Класс Use Case для получения пагинированного списка значений модификаций.

    Использует:
        - Репозиторий `ModificationValueRepository` для работы с базой данных.
        - DTO `ModificationValueWithRelationsRDTO` для возврата данных с отношениями.
        - Фильтр `ModificationValuePaginationFilter` для пагинации и фильтрации.

    Атрибуты:
        repository (ModificationValueRepository): Репозиторий для работы со значениями модификаций.

    Методы:
        execute(filter: ModificationValuePaginationFilter) -> PaginationModificationValueWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список значений модификаций.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ModificationValueRepository(db)

    async def execute(self, filter: ModificationValuePaginationFilter) -> PaginationModificationValueWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка значений модификаций.

        Args:
            filter (ModificationValuePaginationFilter): Фильтр пагинации с параметрами поиска и сортировки.

        Returns:
            PaginationModificationValueWithRelationsRDTO: Объект пагинации со значениями модификаций.
        """
        pagination = await self.repository.paginate(
            dto=ModificationValueWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return pagination

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """