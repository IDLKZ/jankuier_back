from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import AcademyGroupEntity
from app.shared.query_constants import AppQueryConstants


class AcademyGroupPaginationFilter(BasePaginationFilter[AcademyGroupEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество групп академий на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по названию, описанию группы"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        academy_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по академиям"
        ),
        gender: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Фильтрация по полу (0-любой, 1-мужской, 2-женский)"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по статусу активности"
        ),
        is_recruiting: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по статусу набора"
        ),
        min_age_from: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Минимальный возраст от"
        ),
        min_age_to: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Минимальный возраст до"
        ),
        max_age_from: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Максимальный возраст от"
        ),
        max_age_to: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Максимальный возраст до"
        ),
        price_from: float | None = AppQueryConstants.StandardOptionalDecimalQuery(
            "Цена от"
        ),
        price_to: float | None = AppQueryConstants.StandardOptionalDecimalQuery(
            "Цена до"
        ),
        has_free_space: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по наличию свободных мест"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=AcademyGroupEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.academy_ids = academy_ids
        self.gender = gender
        self.is_active = is_active
        self.is_recruiting = is_recruiting
        self.min_age_from = min_age_from
        self.min_age_to = min_age_to
        self.max_age_from = max_age_from
        self.max_age_to = max_age_to
        self.price_from = price_from
        self.price_to = price_to
        self.has_free_space = has_free_space
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return [
            "name",
            "description_ru",
            "description_kk",
            "description_en",
            "value",
            "price_per_ru",
            "price_per_kk",
            "price_per_en",
        ]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.academy_ids:
            filters.append(AcademyGroupEntity.academy_id.in_(self.academy_ids))

        if self.gender is not None:
            filters.append(AcademyGroupEntity.gender == self.gender)

        if self.is_active is not None:
            filters.append(AcademyGroupEntity.is_active == self.is_active)

        if self.is_recruiting is not None:
            filters.append(AcademyGroupEntity.is_recruiting == self.is_recruiting)

        if self.min_age_from is not None:
            filters.append(AcademyGroupEntity.min_age >= self.min_age_from)

        if self.min_age_to is not None:
            filters.append(AcademyGroupEntity.min_age <= self.min_age_to)

        if self.max_age_from is not None:
            filters.append(AcademyGroupEntity.max_age >= self.max_age_from)

        if self.max_age_to is not None:
            filters.append(AcademyGroupEntity.max_age <= self.max_age_to)

        if self.price_from is not None:
            filters.append(AcademyGroupEntity.price >= self.price_from)

        if self.price_to is not None:
            filters.append(AcademyGroupEntity.price <= self.price_to)

        if self.has_free_space is not None:
            if self.has_free_space:
                filters.append(AcademyGroupEntity.free_space > 0)
            else:
                filters.append(AcademyGroupEntity.free_space == 0)

        return filters
