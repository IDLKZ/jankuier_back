from sqlalchemy import inspect, or_, exists, select
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import NotificationEntity, ReadNotificationEntity
from app.shared.query_constants import AppQueryConstants


class NotificationPaginationFilter(BasePaginationFilter[NotificationEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество элементов на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по заголовку и описанию уведомления"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле для сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        topic_id: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Фильтрация по топику уведомления"
        ),
        user_id: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Фильтрация по пользователю"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности уведомления"
        ),
        is_read: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по прочитанным уведомлениям (для конкретного пользователя)"
        ),
        current_user_id: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "ID текущего пользователя для фильтрации is_read"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=NotificationEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.topic_id = topic_id
        self.user_id = user_id
        self.is_active = is_active
        self.is_read = is_read
        self.current_user_id = current_user_id
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return [
            "title_ru",
            "title_kk",
            "title_en",
            "description_ru",
            "description_kk",
            "description_en",
        ]

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

        if self.topic_id is not None:
            filters.append(self.model.topic_id == self.topic_id)

        if self.user_id is not None:
            filters.append(self.model.user_id == self.user_id)

        if self.is_active is not None:
            filters.append(self.model.is_active.is_(self.is_active))

        # Фильтр по прочитанным/непрочитанным уведомлениям
        if self.is_read is not None and self.current_user_id is not None:
            read_exists = exists(
                select(ReadNotificationEntity.id).where(
                    ReadNotificationEntity.notification_id == self.model.id,
                    ReadNotificationEntity.user_id == self.current_user_id,
                )
            )
            if self.is_read:
                filters.append(read_exists)
            else:
                filters.append(~read_exists)

        return filters
