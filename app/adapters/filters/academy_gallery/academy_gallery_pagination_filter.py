from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import AcademyGalleryEntity
from app.shared.query_constants import AppQueryConstants


class AcademyGalleryPaginationFilter(BasePaginationFilter[AcademyGalleryEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество изображений галереи академий на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
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
            model=AcademyGalleryEntity,
            search=None,  # В таблице нет строковых полей для поиска
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.academy_ids = academy_ids
        self.group_ids = group_ids
        self.file_ids = file_ids
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return []  # В таблице нет строковых полей для текстового поиска

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.academy_ids:
            filters.append(AcademyGalleryEntity.academy_id.in_(self.academy_ids))

        if self.group_ids:
            filters.append(AcademyGalleryEntity.group_id.in_(self.group_ids))

        if self.file_ids:
            filters.append(AcademyGalleryEntity.file_id.in_(self.file_ids))

        return filters