from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import AcademyMaterialEntity
from app.shared.query_constants import AppQueryConstants


class AcademyMaterialFilter(BaseFilter[AcademyMaterialEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardSearchQuery("Поиск по названию материала"),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        academy_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по академиям"),
        group_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по группам академий"),
        file_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по файлам"),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=AcademyMaterialEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.academy_ids = academy_ids
        self.group_ids = group_ids
        self.file_ids = file_ids
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["title"]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.academy_ids:
            filters.append(AcademyMaterialEntity.academy_id.in_(self.academy_ids))

        if self.group_ids:
            filters.append(AcademyMaterialEntity.group_id.in_(self.group_ids))

        if self.file_ids:
            filters.append(AcademyMaterialEntity.file_id.in_(self.file_ids))

        return filters