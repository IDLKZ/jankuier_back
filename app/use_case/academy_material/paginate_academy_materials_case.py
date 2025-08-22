from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_material.academy_material_dto import (
    AcademyMaterialWithRelationsRDTO,
    PaginationAcademyMaterialWithRelationsRDTO,
)
from app.adapters.filters.academy_material.academy_material_pagination_filter import (
    AcademyMaterialPaginationFilter,
)
from app.adapters.repository.academy_material.academy_material_repository import (
    AcademyMaterialRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateAcademyMaterialsCase(
    BaseUseCase[PaginationAcademyMaterialWithRelationsRDTO]
):
    """
    Класс Use Case для получения материалов академий с пагинацией.

    Использует:
        - Репозиторий `AcademyMaterialRepository` для работы с базой данных.
        - Фильтр `AcademyMaterialPaginationFilter` для пагинации и фильтрации.
        - DTO `PaginationAcademyMaterialWithRelationsRDTO` для возврата пагинированных данных.

    Атрибуты:
        repository (AcademyMaterialRepository): Репозиторий для работы с материалами академий.

    Методы:
        execute(filter: AcademyMaterialPaginationFilter) -> PaginationAcademyMaterialWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список материалов академий.
        validate(filter: AcademyMaterialPaginationFilter):
            Валидация входных параметров.
        transform():
            Преобразование данных (не используется в данном случае).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyMaterialRepository(db)

    async def execute(
        self, filter: AcademyMaterialPaginationFilter
    ) -> PaginationAcademyMaterialWithRelationsRDTO:
        """
        Выполняет операцию получения материалов академий с пагинацией.

        Args:
            filter (AcademyMaterialPaginationFilter): Объект фильтра с параметрами пагинации.

        Returns:
            PaginationAcademyMaterialWithRelationsRDTO: Пагинированный список материалов академий.
        """
        await self.validate(filter)

        # Получаем пагинированные данные
        pagination = await self.repository.paginate(
            dto=AcademyMaterialWithRelationsRDTO,
            filters=filter.apply(),
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by or "created_at",
            order_direction=filter.order_direction or "desc",
            include_deleted_filter=not filter.is_show_deleted,
            options=self.repository.default_relationships(),
        )

        return pagination

    async def validate(self, filter: AcademyMaterialPaginationFilter) -> None:
        """
        Валидация входных параметров.

        Args:
            filter (AcademyMaterialPaginationFilter): Фильтр для валидации.
        """
        pass

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass