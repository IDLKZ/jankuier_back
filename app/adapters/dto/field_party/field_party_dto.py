from pydantic import BaseModel
from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.field.field_dto import FieldRDTO
from app.shared.dto_constants import DTOConstant


class FieldPartyDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class FieldPartyCDTO(BaseModel):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID изображения площадки"
    )
    field_id: DTOConstant.StandardUnsignedIntegerField(description="ID поля")
    title_ru: DTOConstant.StandardVarcharField(
        description="Название площадки на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название площадки на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название площадки на английском"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение площадки"
    )
    person_qty: DTOConstant.StandardIntegerField(description="Количество людей")
    length_m: DTOConstant.StandardIntegerField(description="Длина в метрах")
    width_m: DTOConstant.StandardIntegerField(description="Ширина в метрах")
    deepth_m: DTOConstant.StandardNullableIntegerField(description="Глубина в метрах")
    latitude: DTOConstant.StandardNullableVarcharField(description="Широта")
    longitude: DTOConstant.StandardNullableVarcharField(description="Долгота")
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Флаг активности площадки"
    )
    is_covered: DTOConstant.StandardBooleanFalseField(description="Наличие крыши")
    is_default: DTOConstant.StandardBooleanFalseField(
        description="Площадка по умолчанию"
    )
    cover_type: DTOConstant.StandardTinyIntegerField(description="Тип покрытия")

    class Config:
        from_attributes = True


class FieldPartyRDTO(FieldPartyDTO):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID изображения площадки"
    )
    field_id: DTOConstant.StandardUnsignedIntegerField(description="ID поля")
    title_ru: DTOConstant.StandardVarcharField(
        description="Название площадки на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название площадки на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название площадки на английском"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение площадки"
    )
    person_qty: DTOConstant.StandardIntegerField(description="Количество людей")
    length_m: DTOConstant.StandardIntegerField(description="Длина в метрах")
    width_m: DTOConstant.StandardIntegerField(description="Ширина в метрах")
    deepth_m: DTOConstant.StandardNullableIntegerField(description="Глубина в метрах")
    latitude: DTOConstant.StandardNullableVarcharField(description="Широта")
    longitude: DTOConstant.StandardNullableVarcharField(description="Долгота")
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Флаг активности площадки"
    )
    is_covered: DTOConstant.StandardBooleanFalseField(description="Наличие крыши")
    is_default: DTOConstant.StandardBooleanFalseField(
        description="Площадка по умолчанию"
    )
    cover_type: DTOConstant.StandardTinyIntegerField(description="Тип покрытия")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class FieldPartyWithRelationsRDTO(FieldPartyRDTO):
    image: FileRDTO | None = None
    field: FieldRDTO | None = None

    class Config:
        from_attributes = True


class FieldPartyUpdateDTO(BaseModel):
    """DTO для обновления площадки - все поля опциональные"""

    image_id: (
        DTOConstant.StandardNullableUnsignedIntegerField(
            description="ID изображения площадки"
        )
        | None
    ) = None
    title_ru: (
        DTOConstant.StandardVarcharField(description="Название площадки на русском")
        | None
    ) = None
    title_kk: (
        DTOConstant.StandardNullableVarcharField(
            description="Название площадки на казахском"
        )
        | None
    ) = None
    title_en: (
        DTOConstant.StandardNullableVarcharField(
            description="Название площадки на английском"
        )
        | None
    ) = None
    person_qty: (
        DTOConstant.StandardIntegerField(description="Количество людей") | None
    ) = None
    length_m: DTOConstant.StandardIntegerField(description="Длина в метрах") | None = (
        None
    )
    width_m: DTOConstant.StandardIntegerField(description="Ширина в метрах") | None = (
        None
    )
    deepth_m: (
        DTOConstant.StandardNullableIntegerField(description="Глубина в метрах") | None
    ) = None
    latitude: DTOConstant.StandardNullableVarcharField(description="Широта") | None = (
        None
    )
    longitude: (
        DTOConstant.StandardNullableVarcharField(description="Долгота") | None
    ) = None
    is_active: (
        DTOConstant.StandardBooleanTrueField(description="Флаг активности площадки")
        | None
    ) = None
    is_covered: (
        DTOConstant.StandardBooleanFalseField(description="Наличие крыши") | None
    ) = None
    is_default: (
        DTOConstant.StandardBooleanFalseField(description="Площадка по умолчанию")
        | None
    ) = None
    cover_type: (
        DTOConstant.StandardTinyIntegerField(description="Тип покрытия") | None
    ) = None

    class Config:
        from_attributes = True
