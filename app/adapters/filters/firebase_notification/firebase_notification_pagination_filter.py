from sqlalchemy import inspect, or_
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import FirebaseNotificationEntity
from app.shared.query_constants import AppQueryConstants


class FirebaseNotificationPaginationFilter(BasePaginationFilter[FirebaseNotificationEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество элементов на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по токену"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле для сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        user_id: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Фильтрация по пользователю"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности токена"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=FirebaseNotificationEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.user_id = user_id
        self.is_active = is_active
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["token"]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.search:
            model_columns = {c.key for c in inspect(self.model).columns}
            search_fields = self.get_search_filters()
            valid_fields = [f for f in search_fields if f in model_columns]

            if valid_fields:
                filters.append(
                    or_(
                        *[
                            getattr(self.model, field).ilike(f"%{self.search}%")
                            for field in valid_fields
                        ]
                    )
                )

        if self.user_id is not None:
            filters.append(self.model.user_id == self.user_id)

        if self.is_active is not None:
            filters.append(self.model.is_active.is_(self.is_active))

        return filters
