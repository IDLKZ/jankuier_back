from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import RolePermissionEntity
from app.shared.query_constants import AppQueryConstants


class RolePermissionFilter(BaseFilter[RolePermissionEntity]):
    def __init__(
        self,
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        role_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по ролям"),
        permission_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по разрешениям"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=RolePermissionEntity,
            search=None,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.role_ids = role_ids
        self.permission_ids = permission_ids
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return []  # В таблице нет строковых полей для текстового поиска

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.role_ids:
            filters.append(RolePermissionEntity.role_id.in_(self.role_ids))

        if self.permission_ids:
            filters.append(RolePermissionEntity.permission_id.in_(self.permission_ids))

        return filters
