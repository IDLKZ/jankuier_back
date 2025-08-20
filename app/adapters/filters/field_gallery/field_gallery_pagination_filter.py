from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import FieldGalleryEntity
from app.shared.query_constants import AppQueryConstants


class FieldGalleryPaginationFilter(BasePaginationFilter[FieldGalleryEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество изображений галереи на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        field_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по полям"),
        party_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по площадкам"),
        file_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по файлам"),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=FieldGalleryEntity,
            search=None,  # В таблице нет строковых полей для поиска
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.field_ids = field_ids
        self.party_ids = party_ids
        self.file_ids = file_ids
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return []  # В таблице нет строковых полей для текстового поиска

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.field_ids:
            filters.append(FieldGalleryEntity.field_id.in_(self.field_ids))

        if self.party_ids:
            filters.append(FieldGalleryEntity.party_id.in_(self.party_ids))

        if self.file_ids:
            filters.append(FieldGalleryEntity.file_id.in_(self.file_ids))

        return filters