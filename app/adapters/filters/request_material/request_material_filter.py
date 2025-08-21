from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import RequestMaterialEntity
from app.shared.query_constants import AppQueryConstants


class RequestMaterialFilter(BaseFilter[RequestMaterialEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по названию материала заявки"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        request_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по заявкам в академические группы"
        ),
        student_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по студентам"
        ),
        file_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по файлам"),
        has_file: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по наличию прикрепленного файла"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=RequestMaterialEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.request_ids = request_ids
        self.student_ids = student_ids
        self.file_ids = file_ids
        self.has_file = has_file
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["title"]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.request_ids:
            filters.append(RequestMaterialEntity.request_id.in_(self.request_ids))

        if self.student_ids:
            filters.append(RequestMaterialEntity.student_id.in_(self.student_ids))

        if self.file_ids:
            filters.append(RequestMaterialEntity.file_id.in_(self.file_ids))

        if self.has_file is not None:
            if self.has_file:
                filters.append(RequestMaterialEntity.file_id.is_not(None))
            else:
                filters.append(RequestMaterialEntity.file_id.is_(None))

        return filters
