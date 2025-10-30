from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import YandexAfishaWidgetTicketEntity
from app.shared.query_constants import AppQueryConstants


class YandexAfishaWidgetTicketFilter(BaseFilter[YandexAfishaWidgetTicketEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по названию, описанию, адресу, стадиону"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по статусу активности"
        ),
        start_at_from: str | None = AppQueryConstants.StandardOptionalDateTimeQuery(
            "Дата начала мероприятия от"
        ),
        start_at_to: str | None = AppQueryConstants.StandardOptionalDateTimeQuery(
            "Дата начала мероприятия до"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=YandexAfishaWidgetTicketEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.is_active = is_active
        self.start_at_from = start_at_from
        self.start_at_to = start_at_to
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return [
            "title_ru",
            "title_kk",
            "title_en",
            "description_ru",
            "description_kk",
            "description_en",
            "address_ru",
            "address_kk",
            "address_en",
            "stadium_ru",
            "stadium_kk",
            "stadium_en",
            "yandex_session_id",
        ]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.is_active is not None:
            filters.append(YandexAfishaWidgetTicketEntity.is_active == self.is_active)

        if self.start_at_from is not None:
            filters.append(
                YandexAfishaWidgetTicketEntity.start_at >= self.start_at_from
            )

        if self.start_at_to is not None:
            filters.append(YandexAfishaWidgetTicketEntity.start_at <= self.start_at_to)

        return filters
