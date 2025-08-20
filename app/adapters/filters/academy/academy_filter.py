from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import AcademyEntity
from app.shared.query_constants import AppQueryConstants


class AcademyFilter(BaseFilter[AcademyEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery("Поиск по названию, описанию, адресу"),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        city_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по городам"),
        gender: (
            int | None
        ) = AppQueryConstants.StandardOptionalIntegerQuery("Фильтрация по полу (0-любой, 1-мужской, 2-женский)"),
        is_active: (
            bool | None
        ) = AppQueryConstants.StandardOptionalBooleanQuery("Фильтрация по статусу активности"),
        min_age_from: (
            int | None
        ) = AppQueryConstants.StandardOptionalIntegerQuery("Минимальный возраст от"),
        min_age_to: (
            int | None
        ) = AppQueryConstants.StandardOptionalIntegerQuery("Минимальный возраст до"),
        max_age_from: (
            int | None
        ) = AppQueryConstants.StandardOptionalIntegerQuery("Максимальный возраст от"),
        max_age_to: (
            int | None
        ) = AppQueryConstants.StandardOptionalIntegerQuery("Максимальный возраст до"),
        average_price_from: (
            float | None
        ) = AppQueryConstants.StandardOptionalDecimalQuery("Средняя цена от"),
        average_price_to: (
            float | None
        ) = AppQueryConstants.StandardOptionalDecimalQuery("Средняя цена до"),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=AcademyEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.city_ids = city_ids
        self.gender = gender
        self.is_active = is_active
        self.min_age_from = min_age_from
        self.min_age_to = min_age_to
        self.max_age_from = max_age_from
        self.max_age_to = max_age_to
        self.average_price_from = average_price_from
        self.average_price_to = average_price_to
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
            "value",
            "phone",
            "email"
        ]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.city_ids:
            filters.append(AcademyEntity.city_id.in_(self.city_ids))

        if self.gender is not None:
            filters.append(AcademyEntity.gender == self.gender)

        if self.is_active is not None:
            filters.append(AcademyEntity.is_active == self.is_active)

        if self.min_age_from is not None:
            filters.append(AcademyEntity.min_age >= self.min_age_from)

        if self.min_age_to is not None:
            filters.append(AcademyEntity.min_age <= self.min_age_to)

        if self.max_age_from is not None:
            filters.append(AcademyEntity.max_age >= self.max_age_from)

        if self.max_age_to is not None:
            filters.append(AcademyEntity.max_age <= self.max_age_to)

        if self.average_price_from is not None:
            filters.append(AcademyEntity.average_price >= self.average_price_from)

        if self.average_price_to is not None:
            filters.append(AcademyEntity.average_price <= self.average_price_to)

        return filters