from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import RequestToAcademyGroupEntity
from app.shared.query_constants import AppQueryConstants


class RequestToAcademyGroupFilter(BaseFilter[RequestToAcademyGroupEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery("Поиск по информации о заявке"),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        student_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по студентам"),
        group_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по группам академий"),
        checked_by_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по проверившим заявку"),
        status: (
            int | None
        ) = AppQueryConstants.StandardOptionalIntegerQuery("Фильтрация по статусу (0-не просмотрена, 1-принята, -1-отклонена)"),
        statuses: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по статусам (0-не просмотрена, 1-принята, -1-отклонена)"),
        is_checked: (
            bool | None
        ) = AppQueryConstants.StandardOptionalBooleanQuery("Фильтрация по факту проверки заявки"),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=RequestToAcademyGroupEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.student_ids = student_ids
        self.group_ids = group_ids
        self.checked_by_ids = checked_by_ids
        self.status = status
        self.statuses = statuses
        self.is_checked = is_checked
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["info"]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.student_ids:
            filters.append(RequestToAcademyGroupEntity.student_id.in_(self.student_ids))

        if self.group_ids:
            filters.append(RequestToAcademyGroupEntity.group_id.in_(self.group_ids))

        if self.checked_by_ids:
            filters.append(RequestToAcademyGroupEntity.checked_by.in_(self.checked_by_ids))

        if self.status is not None:
            filters.append(RequestToAcademyGroupEntity.status == self.status)

        if self.statuses:
            filters.append(RequestToAcademyGroupEntity.status.in_(self.statuses))

        if self.is_checked is not None:
            if self.is_checked:
                filters.append(RequestToAcademyGroupEntity.checked_by.is_not(None))
            else:
                filters.append(RequestToAcademyGroupEntity.checked_by.is_(None))

        return filters