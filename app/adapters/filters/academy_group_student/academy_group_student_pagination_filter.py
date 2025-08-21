from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import AcademyGroupStudentEntity
from app.shared.query_constants import AppQueryConstants


class AcademyGroupStudentPaginationFilter(
    BasePaginationFilter[AcademyGroupStudentEntity]
):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество записей студентов в группах академий на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по информации о студенте в группе"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        student_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по студентам"
        ),
        group_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по группам академий"
        ),
        request_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по заявкам в академические группы"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по статусу активности студента в группе"
        ),
        has_request: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по наличию связанной заявки"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=AcademyGroupStudentEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.student_ids = student_ids
        self.group_ids = group_ids
        self.request_ids = request_ids
        self.is_active = is_active
        self.has_request = has_request
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["info"]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.student_ids:
            filters.append(AcademyGroupStudentEntity.student_id.in_(self.student_ids))

        if self.group_ids:
            filters.append(AcademyGroupStudentEntity.group_id.in_(self.group_ids))

        if self.request_ids:
            filters.append(AcademyGroupStudentEntity.request_id.in_(self.request_ids))

        if self.is_active is not None:
            filters.append(AcademyGroupStudentEntity.is_active == self.is_active)

        if self.has_request is not None:
            if self.has_request:
                filters.append(AcademyGroupStudentEntity.request_id.is_not(None))
            else:
                filters.append(AcademyGroupStudentEntity.request_id.is_(None))

        return filters
