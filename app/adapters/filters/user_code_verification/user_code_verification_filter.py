from sqlalchemy import or_, func

from app.adapters.filters.base_filter import BaseFilter
from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities.user_code_verification_entity import UserCodeVerificationEntity


class UserCodeVerificationFilter(BaseFilter):
    """Фильтр для кодов верификации пользователей"""

    def __init__(
        self,
        search: str | None = None,
        user_id: int | None = None,
        code: str | None = None,
        order_by: str = "created_at",
        order_direction: str = "desc",
        is_show_deleted: bool = False,
    ):
        super().__init__(
            model=UserCodeVerificationEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.is_show_deleted=is_show_deleted,
        self.user_id = user_id
        self.code = code

    def get_search_filters(self) -> list[str] | None:
        return [
            "code",
        ]

    def apply(self) -> list:
        """Применить фильтры"""
        filters = []

        # Поиск по коду
        if self.search:
            filters.append(
                or_(
                    UserCodeVerificationEntity.code.ilike(f"%{self.search}%"),
                )
            )

        # Фильтр по user_id
        if self.user_id:
            filters.append(UserCodeVerificationEntity.user_id == self.user_id)

        # Фильтр по коду
        if self.code:
            filters.append(func.lower(UserCodeVerificationEntity.code) == func.lower(self.code))

        return filters


class UserCodeVerificationPaginationFilter(BasePaginationFilter):
    """Пагинационный фильтр для кодов верификации"""

    def __init__(
        self,
        page: int = 1,
        per_page: int = 20,
        search: str | None = None,
        user_id: int | None = None,
        code: str | None = None,
        order_by: str = "created_at",
        order_direction: str = "desc",
        is_show_deleted: bool = False,
    ):
        super().__init__(
            model=UserCodeVerificationEntity,
            page=page,
            per_page=per_page,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.is_show_deleted=is_show_deleted
        self.user_id = user_id
        self.code = code

    def get_search_filters(self) -> list[str] | None:
        return [
            "code",
        ]

    def apply(self) -> list:
        """Применить фильтры"""
        filters = []

        # Поиск по коду
        if self.search:
            filters.append(
                or_(
                    UserCodeVerificationEntity.code.ilike(f"%{self.search}%"),
                )
            )

        # Фильтр по user_id
        if self.user_id:
            filters.append(UserCodeVerificationEntity.user_id == self.user_id)

        # Фильтр по коду
        if self.code:
            filters.append(func.lower(UserCodeVerificationEntity.code) == func.lower(self.code))

        return filters
