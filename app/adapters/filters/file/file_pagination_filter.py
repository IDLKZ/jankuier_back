from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import FileEntity
from app.shared.query_constants import AppQueryConstants


class FilePaginationFilter(BasePaginationFilter[FileEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(),
        page: int = AppQueryConstants.StandardPageQuery(),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            description="Поиск по имени файла, пути или MIME-типу"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(),
        is_remote: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            description="Удалённый файл?"
        ),
    ) -> None:
        super().__init__(
            model=FileEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.is_remote = is_remote

    def get_search_filters(self) -> list[str] | None:
        return [
            "filename",
            "file_path",
            "content_type",
        ]

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

        if self.is_remote is not None:
            filters.append(self.model.is_remote == self.is_remote)

        return filters
