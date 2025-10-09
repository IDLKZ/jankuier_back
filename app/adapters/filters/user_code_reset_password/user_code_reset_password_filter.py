from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities.user_reset_password_code_entity import UserCodeResetPasswordEntity
from app.shared.query_constants import AppQueryConstants


class UserCodeResetPasswordFilter(BaseFilter[UserCodeResetPasswordEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по коду"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        user_id: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Фильтрация по ID пользователя"
        ),
    ) -> None:
        super().__init__(
            model=UserCodeResetPasswordEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.user_id = user_id

    def get_search_filters(self) -> list[str] | None:
        return ["code"]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.search:
            model_columns = {column.key for column in inspect(self.model).columns}
            valid_fields = [
                field for field in self.get_search_filters() if field in model_columns
            ]
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

        return filters
