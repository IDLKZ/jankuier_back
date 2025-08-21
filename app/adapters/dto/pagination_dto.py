from typing import Generic, TypeVar

from pydantic import BaseModel

from app.adapters.dto.permission.permission_dto import PermissionRDTO
from app.adapters.dto.country.country_dto import CountryRDTO
from app.adapters.dto.city.city_dto import CityRDTO, CityWithRelationsRDTO
from app.adapters.dto.sport.sport_dto import SportRDTO
from app.adapters.dto.product_category.product_category_dto import ProductCategoryRDTO, ProductCategoryWithRelationsRDTO
from app.adapters.dto.field.field_dto import FieldRDTO, FieldWithRelationsRDTO
from app.adapters.dto.field_party.field_party_dto import FieldPartyRDTO, FieldPartyWithRelationsRDTO
from app.adapters.dto.field_party_schedule_settings.field_party_schedule_settings_dto import FieldPartyScheduleSettingsRDTO, FieldPartyScheduleSettingsWithRelationsRDTO
from app.adapters.dto.field_party_schedule.field_party_schedule_dto import FieldPartyScheduleRDTO, FieldPartyScheduleWithRelationsRDTO
from app.adapters.dto.field_gallery.field_gallery_dto import FieldGalleryRDTO, FieldGalleryWithRelationsRDTO
from app.adapters.dto.academy.academy_dto import AcademyRDTO, AcademyWithRelationsRDTO
from app.adapters.dto.product.product_dto import ProductRDTO, ProductWithRelationsRDTO
from app.adapters.dto.modification_type.modification_type_dto import ModificationTypeRDTO
from app.adapters.dto.product_variant.product_variant_dto import ProductVariantRDTO, ProductVariantWithRelationsRDTO
from app.adapters.dto.modification_value.modification_value_dto import ModificationValueRDTO, ModificationValueWithRelationsRDTO
from app.adapters.dto.product_variant_modification.product_variant_modification_dto import ProductVariantModificationRDTO, ProductVariantModificationWithRelationsRDTO
from app.adapters.dto.category_modification.category_modification_dto import CategoryModificationRDTO, CategoryModificationWithRelationsRDTO
from app.adapters.dto.product_gallery.product_gallery_dto import ProductGalleryRDTO, ProductGalleryWithRelationsRDTO
from app.adapters.dto.student.student_dto import StudentRDTO, StudentWithRelationsRDTO
from app.adapters.dto.request_to_academy_group.request_to_academy_group_dto import RequestToAcademyGroupRDTO, RequestToAcademyGroupWithRelationsRDTO
from app.adapters.dto.request_material.request_material_dto import RequestMaterialRDTO, RequestMaterialWithRelationsRDTO
from app.adapters.dto.academy_group_student.academy_group_student_dto import AcademyGroupStudentRDTO, AcademyGroupStudentWithRelationsRDTO

T = TypeVar("T")


class Pagination(Generic[T]):
    """
    Обобщенная модель пагинации.

    Атрибуты:
        current_page (int): Текущая страница.
        last_page (int): Последняя страница.
        total_pages (int): Общее количество страниц.
        total_items (int): Общее количество элементов.
        items (list[T]): Список элементов текущей страницы.
    """

    current_page: int
    per_page: int
    last_page: int
    total_pages: int
    total_items: int
    items: list[T]

    def __init__(
        self,
        items: list[T],
        total_pages: int,
        total_items: int,
        per_page: int,
        page: int,
    ) -> None:
        self.items = items
        self.total_pages = total_pages
        self.total_items = total_items
        self.current_page = page
        self.per_page = per_page
        self.last_page = (total_pages + per_page - 1) // per_page


class BasePageModel(BaseModel):
    """
    Базовая модель пагинации.
    Атрибуты:
       current_page (int): Текущая страница.
       last_page (int): Последняя страница.
       total_pages (int): Общее количество страниц.
       total_items (int): Общее количество элементов.
       items (list[T]): Список элементов текущей страницы.
    """

    current_page: int
    per_page: int
    last_page: int
    total_pages: int
    total_items: int


class PaginationPermissionRDTO(BasePageModel):
    items: list[PermissionRDTO]


class PaginationCountryRDTO(BasePageModel):
    items: list[CountryRDTO]


class PaginationCityRDTO(BasePageModel):
    items: list[CityRDTO]


class PaginationCityWithRelationsRDTO(BasePageModel):
    items: list[CityWithRelationsRDTO]


class PaginationSportRDTO(BasePageModel):
    items: list[SportRDTO]


class PaginationProductCategoryRDTO(BasePageModel):
    items: list[ProductCategoryRDTO]


class PaginationProductCategoryWithRelationsRDTO(BasePageModel):
    items: list[ProductCategoryWithRelationsRDTO]


class PaginationFieldRDTO(BasePageModel):
    items: list[FieldRDTO]


class PaginationFieldWithRelationsRDTO(BasePageModel):
    items: list[FieldWithRelationsRDTO]


class PaginationFieldPartyRDTO(BasePageModel):
    items: list[FieldPartyRDTO]


class PaginationFieldPartyWithRelationsRDTO(BasePageModel):
    items: list[FieldPartyWithRelationsRDTO]


class PaginationFieldPartyScheduleSettingsRDTO(BasePageModel):
    items: list[FieldPartyScheduleSettingsRDTO]


class PaginationFieldPartyScheduleSettingsWithRelationsRDTO(BasePageModel):
    items: list[FieldPartyScheduleSettingsWithRelationsRDTO]


class PaginationFieldPartyScheduleRDTO(BasePageModel):
    items: list[FieldPartyScheduleRDTO]


class PaginationFieldPartyScheduleWithRelationsRDTO(BasePageModel):
    items: list[FieldPartyScheduleWithRelationsRDTO]


class PaginationFieldGalleryRDTO(BasePageModel):
    items: list[FieldGalleryRDTO]


class PaginationFieldGalleryWithRelationsRDTO(BasePageModel):
    items: list[FieldGalleryWithRelationsRDTO]


class PaginationAcademyRDTO(BasePageModel):
    items: list[AcademyRDTO]


class PaginationAcademyWithRelationsRDTO(BasePageModel):
    items: list[AcademyWithRelationsRDTO]


class PaginationProductRDTO(BasePageModel):
    items: list[ProductRDTO]


class PaginationProductWithRelationsRDTO(BasePageModel):
    items: list[ProductWithRelationsRDTO]


class PaginationModificationTypeRDTO(BasePageModel):
    items: list[ModificationTypeRDTO]


class PaginationProductVariantRDTO(BasePageModel):
    items: list[ProductVariantRDTO]


class PaginationProductVariantWithRelationsRDTO(BasePageModel):
    items: list[ProductVariantWithRelationsRDTO]


class PaginationModificationValueRDTO(BasePageModel):
    items: list[ModificationValueRDTO]


class PaginationModificationValueWithRelationsRDTO(BasePageModel):
    items: list[ModificationValueWithRelationsRDTO]


class PaginationProductVariantModificationRDTO(BasePageModel):
    items: list[ProductVariantModificationRDTO]


class PaginationProductVariantModificationWithRelationsRDTO(BasePageModel):
    items: list[ProductVariantModificationWithRelationsRDTO]


class PaginationCategoryModificationRDTO(BasePageModel):
    items: list[CategoryModificationRDTO]


class PaginationCategoryModificationWithRelationsRDTO(BasePageModel):
    items: list[CategoryModificationWithRelationsRDTO]


class PaginationProductGalleryRDTO(BasePageModel):
    items: list[ProductGalleryRDTO]


class PaginationProductGalleryWithRelationsRDTO(BasePageModel):
    items: list[ProductGalleryWithRelationsRDTO]


class PaginationStudentRDTO(BasePageModel):
    items: list[StudentRDTO]


class PaginationStudentWithRelationsRDTO(BasePageModel):
    items: list[StudentWithRelationsRDTO]


class PaginationRequestToAcademyGroupRDTO(BasePageModel):
    items: list[RequestToAcademyGroupRDTO]


class PaginationRequestToAcademyGroupWithRelationsRDTO(BasePageModel):
    items: list[RequestToAcademyGroupWithRelationsRDTO]


class PaginationRequestMaterialRDTO(BasePageModel):
    items: list[RequestMaterialRDTO]


class PaginationRequestMaterialWithRelationsRDTO(BasePageModel):
    items: list[RequestMaterialWithRelationsRDTO]


class PaginationAcademyGroupStudentRDTO(BasePageModel):
    items: list[AcademyGroupStudentRDTO]


class PaginationAcademyGroupStudentWithRelationsRDTO(BasePageModel):
    items: list[AcademyGroupStudentWithRelationsRDTO]

