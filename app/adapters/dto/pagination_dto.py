from typing import TYPE_CHECKING, Any, List

from app.adapters.dto.base_pagination_dto import Pagination, BasePageModel
from app.adapters.dto.product_order.product_order_dto import ProductOrderWithRelationsRDTO
from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemWithRelationsRDTO

if TYPE_CHECKING:
    from app.adapters.dto.permission.permission_dto import PermissionRDTO
    from app.adapters.dto.country.country_dto import CountryRDTO
    from app.adapters.dto.city.city_dto import CityRDTO, CityWithRelationsRDTO
    from app.adapters.dto.sport.sport_dto import SportRDTO
    from app.adapters.dto.product_category.product_category_dto import (
        ProductCategoryRDTO,
        ProductCategoryWithRelationsRDTO,
    )
    from app.adapters.dto.field.field_dto import FieldRDTO, FieldWithRelationsRDTO
    from app.adapters.dto.field_party.field_party_dto import (
        FieldPartyRDTO,
        FieldPartyWithRelationsRDTO,
    )
    from app.adapters.dto.field_party_schedule_settings.field_party_schedule_settings_dto import (
        FieldPartyScheduleSettingsRDTO,
        FieldPartyScheduleSettingsWithRelationsRDTO,
    )
    from app.adapters.dto.field_party_schedule.field_party_schedule_dto import (
        FieldPartyScheduleRDTO,
        FieldPartyScheduleWithRelationsRDTO,
    )
    from app.adapters.dto.field_gallery.field_gallery_dto import (
        FieldGalleryRDTO,
        FieldGalleryWithRelationsRDTO,
    )
    from app.adapters.dto.academy.academy_dto import AcademyRDTO, AcademyWithRelationsRDTO
    from app.adapters.dto.academy_group.academy_group_dto import (
        AcademyGroupRDTO,
        AcademyGroupWithRelationsRDTO,
    )
    from app.adapters.dto.product.product_dto import ProductRDTO, ProductWithRelationsRDTO
    from app.adapters.dto.modification_type.modification_type_dto import (
        ModificationTypeRDTO,
    )
    from app.adapters.dto.product_variant.product_variant_dto import (
        ProductVariantRDTO,
        ProductVariantWithRelationsRDTO,
    )
    from app.adapters.dto.modification_value.modification_value_dto import (
        ModificationValueRDTO,
        ModificationValueWithRelationsRDTO,
    )
    from app.adapters.dto.product_variant_modification.product_variant_modification_dto import (
        ProductVariantModificationRDTO,
        ProductVariantModificationWithRelationsRDTO,
    )
    from app.adapters.dto.category_modification.category_modification_dto import (
        CategoryModificationRDTO,
        CategoryModificationWithRelationsRDTO,
    )
    from app.adapters.dto.product_gallery.product_gallery_dto import (
        ProductGalleryRDTO,
        ProductGalleryWithRelationsRDTO,
    )
    from app.adapters.dto.student.student_dto import StudentRDTO, StudentWithRelationsRDTO
    from app.adapters.dto.request_to_academy_group.request_to_academy_group_dto import (
        RequestToAcademyGroupRDTO,
        RequestToAcademyGroupWithRelationsRDTO,
    )
    from app.adapters.dto.request_material.request_material_dto import (
        RequestMaterialRDTO,
        RequestMaterialWithRelationsRDTO,
    )
    from app.adapters.dto.academy_group_student.academy_group_student_dto import (
        AcademyGroupStudentRDTO,
        AcademyGroupStudentWithRelationsRDTO,
    )
    from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
    from app.adapters.dto.payment_transaction_status.payment_transaction_status_dto import (
        PaymentTransactionStatusWithRelationsRDTO,
    )
    from app.adapters.dto.payment_transaction.payment_transaction_dto import (
        PaymentTransactionWithRelationsRDTO,
    )
    from app.adapters.dto.ticketon_order_status.ticketon_order_status_dto import (
        TicketonOrderStatusWithRelationsRDTO,
    )
    from app.adapters.dto.ticketon_order.ticketon_order_dto import (
        TicketonOrderWithRelationsRDTO,
    )
    from app.adapters.dto.user_code_verification.user_code_verification_dto import (
        UserCodeVerificationRDTO,
        UserCodeVerificationWithRelationsRDTO,
    )


class PaginationPermissionRDTO(BasePageModel):
    items: list[Any]


class PaginationCountryRDTO(BasePageModel):
    items: list[Any]


class PaginationCityRDTO(BasePageModel):
    items: list[Any]


class PaginationCityWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationSportRDTO(BasePageModel):
    items: list[Any]


class PaginationProductCategoryRDTO(BasePageModel):
    items: list[Any]


class PaginationProductCategoryWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationFieldRDTO(BasePageModel):
    items: list[Any]


class PaginationFieldWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationFieldPartyRDTO(BasePageModel):
    items: list[Any]


class PaginationFieldPartyWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationFieldPartyScheduleSettingsRDTO(BasePageModel):
    items: list[Any]


class PaginationFieldPartyScheduleSettingsWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationFieldPartyScheduleRDTO(BasePageModel):
    items: list[Any]


class PaginationFieldPartyScheduleWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationFieldGalleryRDTO(BasePageModel):
    items: list[Any]


class PaginationFieldGalleryWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationAcademyRDTO(BasePageModel):
    items: list[Any]


class PaginationAcademyWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationAcademyGroupRDTO(BasePageModel):
    items: list[Any]


class PaginationAcademyGroupWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationProductRDTO(BasePageModel):
    items: list[Any]


class PaginationProductWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationModificationTypeRDTO(BasePageModel):
    items: list[Any]


class PaginationProductVariantRDTO(BasePageModel):
    items: list[Any]


class PaginationProductVariantWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationModificationValueRDTO(BasePageModel):
    items: list[Any]


class PaginationModificationValueWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationProductVariantModificationRDTO(BasePageModel):
    items: list[Any]


class PaginationProductVariantModificationWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationCategoryModificationRDTO(BasePageModel):
    items: list[Any]


class PaginationCategoryModificationWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationProductGalleryRDTO(BasePageModel):
    items: list[Any]


class PaginationProductGalleryWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationStudentRDTO(BasePageModel):
    items: list[Any]


class PaginationStudentWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationRequestToAcademyGroupRDTO(BasePageModel):
    items: list[Any]


class PaginationRequestToAcademyGroupWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationRequestMaterialRDTO(BasePageModel):
    items: list[Any]


class PaginationRequestMaterialWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationAcademyGroupStudentRDTO(BasePageModel):
    items: list[Any]


class PaginationAcademyGroupStudentWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationUserWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationPaymentTransactionStatusWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationPaymentTransactionWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationTicketonOrderStatusWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationTicketonOrderWithRelationsRDTO(BasePageModel):
    items: list[Any]


class PaginationUserCodeVerificationRDTO(BasePageModel):
    items: list[Any]


class PaginationUserCodeVerificationWithRelationsRDTO(BasePageModel):
    items: list[Any]

class PaginationProductOrderWithRelationsRDTO(BasePageModel):
    """Пагинированный ответ для списка заказов с relationships"""
    items: List[ProductOrderWithRelationsRDTO] = []

    class Config:
        from_attributes = True

class PaginationProductOrderItemWithRelationsRDTO(BasePageModel):
    """Пагинированный ответ для списка элементов заказа с relationships"""
    items: List[ProductOrderItemWithRelationsRDTO] = []

    class Config:
        from_attributes = True
