from sqlalchemy import inspect, or_
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import ReadNotificationEntity
from app.shared.query_constants import AppQueryConstants


class ReadNotificationPaginationFilter(BasePaginationFilter[ReadNotificationEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество элементов на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск (не используется для read notifications)"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле для сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        notification_id: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Фильтрация по ID уведомления"
        ),
        user_id: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Фильтрация по ID пользователя"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=ReadNotificationEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.notification_id = notification_id
        self.user_id = user_id
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return []

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.notification_id is not None:
            filters.append(self.model.notification_id == self.notification_id)

        if self.user_id is not None:
            filters.append(self.model.user_id == self.user_id)

        return filters
