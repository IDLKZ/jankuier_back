from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import FieldPartyEntity, FieldEntity
from app.shared.query_constants import AppQueryConstants


class FieldPartyPaginationFilter(BasePaginationFilter[FieldPartyEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество площадок на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по названию или координатам площадки"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        field_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по полям"),
        min_person_qty: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Минимальное количество человек"
        ),
        max_person_qty: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Максимальное количество человек"
        ),
        min_length_m: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Минимальная длина в метрах"
        ),
        max_length_m: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Максимальная длина в метрах"
        ),
        min_width_m: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Минимальная ширина в метрах"
        ),
        max_width_m: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Максимальная ширина в метрах"
        ),
        cover_type: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Тип покрытия"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности площадки"
        ),
        is_covered: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по наличию крыши"
        ),
        is_default: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по площадке по умолчанию"
        ),
        city_id: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Фильтрация по городу поля"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=FieldPartyEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.field_ids = field_ids
        self.min_person_qty = min_person_qty
        self.max_person_qty = max_person_qty
        self.min_length_m = min_length_m
        self.max_length_m = max_length_m
        self.min_width_m = min_width_m
        self.max_width_m = max_width_m
        self.cover_type = cover_type
        self.is_active = is_active
        self.is_covered = is_covered
        self.is_default = is_default
        self.city_id = city_id
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["title_ru", "title_kk", "title_en", "value", "latitude", "longitude"]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.search:
            search_filters = []

            # Search in FieldPartyEntity fields
            model_columns = {column.key for column in inspect(self.model).columns}
            valid_fields = [
                field for field in self.get_search_filters() if field in model_columns
            ]
            if valid_fields:
                search_filters.extend([
                    getattr(self.model, field).ilike(f"%{self.search}%")
                    for field in valid_fields
                ])

            # Search in related FieldEntity fields
            search_filters.extend([
                FieldPartyEntity.field.has(FieldEntity.title_ru.ilike(f"%{self.search}%")),
                FieldPartyEntity.field.has(FieldEntity.title_kk.ilike(f"%{self.search}%")),
                FieldPartyEntity.field.has(FieldEntity.title_en.ilike(f"%{self.search}%")),
                FieldPartyEntity.field.has(FieldEntity.description_ru.ilike(f"%{self.search}%")),
                FieldPartyEntity.field.has(FieldEntity.description_kk.ilike(f"%{self.search}%")),
                FieldPartyEntity.field.has(FieldEntity.description_en.ilike(f"%{self.search}%"))
            ])

            if search_filters:
                filters.append(or_(*search_filters))

        if self.field_ids:
            filters.append(FieldPartyEntity.field_id.in_(self.field_ids))

        if self.min_person_qty is not None:
            filters.append(FieldPartyEntity.person_qty >= self.min_person_qty)

        if self.max_person_qty is not None:
            filters.append(FieldPartyEntity.person_qty <= self.max_person_qty)

        if self.min_length_m is not None:
            filters.append(FieldPartyEntity.length_m >= self.min_length_m)

        if self.max_length_m is not None:
            filters.append(FieldPartyEntity.length_m <= self.max_length_m)

        if self.min_width_m is not None:
            filters.append(FieldPartyEntity.width_m >= self.min_width_m)

        if self.max_width_m is not None:
            filters.append(FieldPartyEntity.width_m <= self.max_width_m)

        if self.cover_type is not None:
            filters.append(FieldPartyEntity.cover_type == self.cover_type)

        if self.is_active is not None:
            filters.append(self.model.is_active.is_(self.is_active))

        if self.is_covered is not None:
            filters.append(self.model.is_covered.is_(self.is_covered))

        if self.is_default is not None:
            filters.append(self.model.is_default.is_(self.is_default))

        if self.city_id is not None:
            filters.append(FieldPartyEntity.field.has(FieldEntity.city_id == self.city_id))

        return filters
