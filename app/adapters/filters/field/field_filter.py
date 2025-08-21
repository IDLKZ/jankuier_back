from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import FieldEntity
from app.shared.query_constants import AppQueryConstants


class FieldFilter(BaseFilter[FieldEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по названию, описанию, адресу или контактам поля"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        city_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по городам"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности поля"
        ),
        has_cover: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по наличию крыши"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=FieldEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.city_ids = city_ids
        self.is_active = is_active
        self.has_cover = has_cover
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return [
            "title_ru",
            "title_kk",
            "title_en",
            "description_ru",
            "description_kk",
            "description_en",
            "value",
            "address_ru",
            "address_en",
            "address_kk",
            "latitude",
            "longitude",
            "phone",
            "additional_phone",
            "email",
            "whatsapp",
            "telegram",
            "instagram",
            "tiktok",
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

        if self.city_ids:
            filters.append(FieldEntity.city_id.in_(self.city_ids))

        if self.is_active is not None:
            filters.append(self.model.is_active.is_(self.is_active))

        if self.has_cover is not None:
            filters.append(self.model.has_cover.is_(self.has_cover))

        return filters
