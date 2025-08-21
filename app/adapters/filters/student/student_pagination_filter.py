from datetime import date
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import StudentEntity
from app.shared.query_constants import AppQueryConstants


class StudentPaginationFilter(BasePaginationFilter[StudentEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество студентов на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по имени, фамилии, телефону, email"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        created_by_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по создателям"
        ),
        gender: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Фильтрация по полу (0-любой, 1-мужской, 2-женский)"
        ),
        birthdate_from: date | None = AppQueryConstants.StandardOptionalDateQuery(
            "Дата рождения от"
        ),
        birthdate_to: date | None = AppQueryConstants.StandardOptionalDateQuery(
            "Дата рождения до"
        ),
        age_from: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Возраст от"
        ),
        age_to: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Возраст до"
        ),
        has_phone: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по наличию телефона"
        ),
        has_email: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по наличию email"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=StudentEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.created_by_ids = created_by_ids
        self.gender = gender
        self.birthdate_from = birthdate_from
        self.birthdate_to = birthdate_to
        self.age_from = age_from
        self.age_to = age_to
        self.has_phone = has_phone
        self.has_email = has_email
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return [
            "first_name",
            "last_name",
            "patronymic",
            "phone",
            "additional_phone",
            "email",
            "info",
        ]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.created_by_ids:
            filters.append(StudentEntity.created_by.in_(self.created_by_ids))

        if self.gender is not None:
            filters.append(StudentEntity.gender == self.gender)

        if self.birthdate_from:
            filters.append(StudentEntity.birthdate >= self.birthdate_from)

        if self.birthdate_to:
            filters.append(StudentEntity.birthdate <= self.birthdate_to)

        # Возраст рассчитывается от даты рождения
        if self.age_from is not None:
            from sqlalchemy import func

            current_date = func.current_date()
            max_birthdate = current_date - func.make_interval(years=self.age_from)
            filters.append(StudentEntity.birthdate <= max_birthdate)

        if self.age_to is not None:
            from sqlalchemy import func

            current_date = func.current_date()
            min_birthdate = current_date - func.make_interval(years=self.age_to + 1)
            filters.append(StudentEntity.birthdate > min_birthdate)

        if self.has_phone is not None:
            if self.has_phone:
                filters.append(StudentEntity.phone.is_not(None))
            else:
                filters.append(StudentEntity.phone.is_(None))

        if self.has_email is not None:
            if self.has_email:
                filters.append(StudentEntity.email.is_not(None))
            else:
                filters.append(StudentEntity.email.is_(None))

        return filters
