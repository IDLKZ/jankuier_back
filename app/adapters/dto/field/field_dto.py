from __future__ import annotations

from pydantic import BaseModel

from app.adapters.dto.city.city_dto import CityRDTO
from app.adapters.dto.file.file_dto import FileRDTO
from app.shared.dto_constants import DTOConstant


class FieldDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class FieldCDTO(BaseModel):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID главного изображения поля"
    )
    city_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID города")
    title_ru: DTOConstant.StandardVarcharField(description="Название поля на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название поля на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название поля на английском"
    )
    description_ru: DTOConstant.StandardNullableTextField(
        description="Описание поля на русском"
    )
    description_kk: DTOConstant.StandardNullableTextField(
        description="Описание поля на казахском"
    )
    description_en: DTOConstant.StandardNullableTextField(
        description="Описание поля на английском"
    )
    value: DTOConstant.StandardUniqueValueField(description="Уникальное значение поля")
    address_ru: DTOConstant.StandardNullableVarcharField(description="Адрес на русском")
    address_en: DTOConstant.StandardNullableVarcharField(
        description="Адрес на английском"
    )
    address_kk: DTOConstant.StandardNullableVarcharField(
        description="Адрес на казахском"
    )
    latitude: DTOConstant.StandardNullableVarcharField(description="Широта")
    longitude: DTOConstant.StandardNullableVarcharField(description="Долгота")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности поля")
    has_cover: DTOConstant.StandardBooleanFalseField(description="Наличие крыши")
    phone: DTOConstant.StandardNullableVarcharField(description="Телефон")
    additional_phone: DTOConstant.StandardNullableVarcharField(
        description="Дополнительный телефон"
    )
    email: DTOConstant.StandardNullableVarcharField(description="Email")
    whatsapp: DTOConstant.StandardNullableVarcharField(description="WhatsApp")
    telegram: DTOConstant.StandardNullableVarcharField(description="Telegram")
    instagram: DTOConstant.StandardNullableVarcharField(description="Instagram")
    tiktok: DTOConstant.StandardNullableVarcharField(description="TikTok")

    class Config:
        from_attributes = True


class FieldRDTO(FieldDTO):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID главного изображения поля"
    )
    city_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID города")
    title_ru: DTOConstant.StandardVarcharField(description="Название поля на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название поля на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название поля на английском"
    )
    description_ru: DTOConstant.StandardNullableTextField(
        description="Описание поля на русском"
    )
    description_kk: DTOConstant.StandardNullableTextField(
        description="Описание поля на казахском"
    )
    description_en: DTOConstant.StandardNullableTextField(
        description="Описание поля на английском"
    )
    value: DTOConstant.StandardUniqueValueField(description="Уникальное значение поля")
    address_ru: DTOConstant.StandardNullableVarcharField(description="Адрес на русском")
    address_en: DTOConstant.StandardNullableVarcharField(
        description="Адрес на английском"
    )
    address_kk: DTOConstant.StandardNullableVarcharField(
        description="Адрес на казахском"
    )
    latitude: DTOConstant.StandardNullableVarcharField(description="Широта")
    longitude: DTOConstant.StandardNullableVarcharField(description="Долгота")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности поля")
    has_cover: DTOConstant.StandardBooleanFalseField(description="Наличие крыши")
    phone: DTOConstant.StandardNullableVarcharField(description="Телефон")
    additional_phone: DTOConstant.StandardNullableVarcharField(
        description="Дополнительный телефон"
    )
    email: DTOConstant.StandardNullableVarcharField(description="Email")
    whatsapp: DTOConstant.StandardNullableVarcharField(description="WhatsApp")
    telegram: DTOConstant.StandardNullableVarcharField(description="Telegram")
    instagram: DTOConstant.StandardNullableVarcharField(description="Instagram")
    tiktok: DTOConstant.StandardNullableVarcharField(description="TikTok")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class FieldWithBasicRelationsRDTO(FieldRDTO):
    """DTO для поля с базовыми связями (без field_parties для избежания циклических ссылок)"""
    image: FileRDTO | None = None
    city: CityRDTO | None = None

    class Config:
        from_attributes = True


class FieldWithRelationsRDTO(FieldRDTO):
    image: FileRDTO | None = None
    city: CityRDTO | None = None

    class Config:
        from_attributes = True


class FieldUpdateDTO(BaseModel):
    """DTO для обновления поля - все поля опциональные"""

    image_id: (
            DTOConstant.StandardNullableUnsignedIntegerField(
                description="ID главного изображения поля"
            )
            | None
    ) = None
    city_id: (
            DTOConstant.StandardNullableUnsignedIntegerField(description="ID города") | None
    ) = None
    title_ru: (
            DTOConstant.StandardVarcharField(description="Название поля на русском") | None
    ) = None
    title_kk: (
            DTOConstant.StandardNullableVarcharField(
                description="Название поля на казахском"
            )
            | None
    ) = None
    title_en: (
            DTOConstant.StandardNullableVarcharField(
                description="Название поля на английском"
            )
            | None
    ) = None
    description_ru: (
            DTOConstant.StandardNullableTextField(description="Описание поля на русском")
            | None
    ) = None
    description_kk: (
            DTOConstant.StandardNullableTextField(description="Описание поля на казахском")
            | None
    ) = None
    description_en: (
            DTOConstant.StandardNullableTextField(description="Описание поля на английском")
            | None
    ) = None
    address_ru: (
            DTOConstant.StandardNullableVarcharField(description="Адрес на русском") | None
    ) = None
    address_en: (
            DTOConstant.StandardNullableVarcharField(description="Адрес на английском")
            | None
    ) = None
    address_kk: (
            DTOConstant.StandardNullableVarcharField(description="Адрес на казахском")
            | None
    ) = None
    latitude: DTOConstant.StandardNullableVarcharField(description="Широта") | None = (
        None
    )
    longitude: (
            DTOConstant.StandardNullableVarcharField(description="Долгота") | None
    ) = None
    is_active: (
            DTOConstant.StandardBooleanTrueField(description="Флаг активности поля") | None
    ) = None
    has_cover: (
            DTOConstant.StandardBooleanFalseField(description="Наличие крыши") | None
    ) = None
    phone: DTOConstant.StandardNullableVarcharField(description="Телефон") | None = None
    additional_phone: (
            DTOConstant.StandardNullableVarcharField(description="Дополнительный телефон")
            | None
    ) = None
    email: DTOConstant.StandardNullableVarcharField(description="Email") | None = None
    whatsapp: (
            DTOConstant.StandardNullableVarcharField(description="WhatsApp") | None
    ) = None
    telegram: (
            DTOConstant.StandardNullableVarcharField(description="Telegram") | None
    ) = None
    instagram: (
            DTOConstant.StandardNullableVarcharField(description="Instagram") | None
    ) = None
    tiktok: DTOConstant.StandardNullableVarcharField(description="TikTok") | None = None

    class Config:
        from_attributes = True
