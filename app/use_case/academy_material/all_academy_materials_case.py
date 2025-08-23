from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_material.academy_material_dto import (
    AcademyMaterialWithRelationsRDTO,
)
from app.adapters.filters.base_filter import BaseFilter
from app.adapters.repository.academy_material.academy_material_repository import (
    AcademyMaterialRepository,
)
from app.use_case.base_case import BaseUseCase


class AllAcademyMaterialsCase(BaseUseCase[list[AcademyMaterialWithRelationsRDTO]]):
    """
    Класс Use Case для получения всех материалов академий с фильтрацией.

    Использует:
        - Репозиторий `AcademyMaterialRepository` для работы с базой данных.
        - Фильтр `BaseFilter` для применения условий поиска и сортировки.
        - DTO `AcademyMaterialWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyMaterialRepository): Репозиторий для работы с материалами академий.

    Методы:
        execute(filter: BaseFilter) -> list[AcademyMaterialWithRelationsRDTO]:
            Выполняет запрос и возвращает список материалов академий.
        validate(filter: BaseFilter):
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
        self, filter: BaseFilter
    ) -> list[AcademyMaterialWithRelationsRDTO]:
        """
        Выполняет операцию получения всех материалов академий с фильтрацией.

        Args:
            filter (BaseFilter): Объект фильтра с параметрами поиска и сортировки.

        Returns:
            list[AcademyMaterialWithRelationsRDTO]: Список материалов академий с связями.
        """
        await self.validate(filter)

        # Применяем фильтры
        filters = []
        if hasattr(filter, "search") and filter.search:
            search_term = f"%{filter.search.lower()}%"
            # Поиск по названию материала и связанным сущностям
            filters.append(
                or_(
                    func.lower(self.repository.model.title).like(search_term),
                    func.lower(self.repository.model.academy.title_ru).like(
                        search_term
                    ),
                    func.lower(self.repository.model.academy.title_kk).like(
                        search_term
                    ),
                    func.lower(self.repository.model.academy.title_en).like(
                        search_term
                    ),
                    func.lower(self.repository.model.group.name).like(search_term),
                    func.lower(self.repository.model.file.filename).like(search_term),
                )
            )

        # Получаем данные из репозитория
        models = await self.repository.get_with_filters(
            filters=filters,
            order_by=getattr(filter, "order_by", "created_at"),
            order_direction=getattr(filter, "order_direction", "desc"),
            include_deleted_filter=not getattr(filter, "is_show_deleted", False),
            options=self.repository.default_relationships(),
        )

        return [AcademyMaterialWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self, filter: BaseFilter) -> None:
        """
        Валидация входных параметров.

        Args:
            filter (BaseFilter): Фильтр для валидации.
        """
        pass

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass