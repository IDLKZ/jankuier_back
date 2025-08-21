from sqlalchemy import or_
from sqlalchemy.orm import Query as SQLAlchemyQuery
from sqlalchemy.inspection import inspect

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import UserEntity
from app.shared.query_constants import AppQueryConstants


class UserPaginationFilter(BasePaginationFilter[UserEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество элементов на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по ИИН, email, телефону, username, имени"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле для сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        role_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по ролям"),
        region_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по регионам"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности"
        ),
        is_verified: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по верификации"
        ),
        sex: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Фильтрация по полу"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=UserEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.role_ids = role_ids
        self.region_ids = region_ids
        self.is_active = is_active
        self.is_verified = is_verified
        self.sex = sex
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return [
            "iin",
            "email",
            "phone",
            "username",
            "first_name",
            "last_name",
            "patronomic",
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

        if self.role_ids:
            filters.append(self.model.role_id.in_(self.role_ids))

        if self.region_ids:
            filters.append(self.model.region_id.in_(self.region_ids))

        if self.is_active is not None:
            filters.append(self.model.is_active.is_(self.is_active))

        if self.is_verified is not None:
            filters.append(self.model.is_verified.is_(self.is_verified))

        if self.sex is not None:
            filters.append(self.model.sex == self.sex)

        return filters
