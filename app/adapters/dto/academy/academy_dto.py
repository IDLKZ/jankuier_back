from pydantic import BaseModel
from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.city.city_dto import CityRDTO
from app.shared.dto_constants import DTOConstant


class AcademyDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class AcademyCDTO(BaseModel):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID главного изображения академии")
    city_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID города")
    title_ru: DTOConstant.StandardVarcharField(description="Название академии на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название академии на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название академии на английском")
    description_ru: DTOConstant.StandardNullableTextField(description="Описание академии на русском")
    description_kk: DTOConstant.StandardNullableTextField(description="Описание академии на казахском")
    description_en: DTOConstant.StandardNullableTextField(description="Описание академии на английском")
    value: DTOConstant.StandardUniqueValueField(description="Уникальное значение академии")
    address_ru: DTOConstant.StandardNullableVarcharField(description="Адрес на русском")
    address_kk: DTOConstant.StandardNullableVarcharField(description="Адрес на казахском")
    address_en: DTOConstant.StandardNullableVarcharField(description="Адрес на английском")
    working_time: DTOConstant.StandardJSONField(description="Рабочее время в формате JSON")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности академии")
    gender: DTOConstant.StandardTinyIntegerField(description="Пол: 0-оба, 1-мужской, 2-женский")
    min_age: DTOConstant.StandardIntegerField(description="Минимальный возраст")
    max_age: DTOConstant.StandardIntegerField(description="Максимальный возраст")
    average_price: DTOConstant.StandardNullableDecimalField(description="Средняя цена")
    average_training_time_in_minute: DTOConstant.StandardNullableIntegerField(description="Среднее время тренировки в минутах")
    phone: DTOConstant.StandardNullableVarcharField(description="Телефон")
    additional_phone: DTOConstant.StandardNullableVarcharField(description="Дополнительный телефон")
    email: DTOConstant.StandardNullableVarcharField(description="Email")
    whatsapp: DTOConstant.StandardNullableVarcharField(description="WhatsApp")
    telegram: DTOConstant.StandardNullableVarcharField(description="Telegram")
    instagram: DTOConstant.StandardNullableVarcharField(description="Instagram")
    tik_tok: DTOConstant.StandardNullableVarcharField(description="TikTok")
    site: DTOConstant.StandardNullableVarcharField(description="Сайт")

    class Config:
        from_attributes = True


class AcademyRDTO(AcademyDTO):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID главного изображения академии")
    city_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID города")
    title_ru: DTOConstant.StandardVarcharField(description="Название академии на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название академии на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название академии на английском")
    description_ru: DTOConstant.StandardNullableTextField(description="Описание академии на русском")
    description_kk: DTOConstant.StandardNullableTextField(description="Описание академии на казахском")
    description_en: DTOConstant.StandardNullableTextField(description="Описание академии на английском")
    value: DTOConstant.StandardUniqueValueField(description="Уникальное значение академии")
    address_ru: DTOConstant.StandardNullableVarcharField(description="Адрес на русском")
    address_kk: DTOConstant.StandardNullableVarcharField(description="Адрес на казахском")
    address_en: DTOConstant.StandardNullableVarcharField(description="Адрес на английском")
    working_time: DTOConstant.StandardJSONField(description="Рабочее время в формате JSON")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности академии")
    gender: DTOConstant.StandardTinyIntegerField(description="Пол: 0-оба, 1-мужской, 2-женский")
    min_age: DTOConstant.StandardIntegerField(description="Минимальный возраст")
    max_age: DTOConstant.StandardIntegerField(description="Максимальный возраст")
    average_price: DTOConstant.StandardNullableDecimalField(description="Средняя цена")
    average_training_time_in_minute: DTOConstant.StandardNullableIntegerField(description="Среднее время тренировки в минутах")
    phone: DTOConstant.StandardNullableVarcharField(description="Телефон")
    additional_phone: DTOConstant.StandardNullableVarcharField(description="Дополнительный телефон")
    email: DTOConstant.StandardNullableVarcharField(description="Email")
    whatsapp: DTOConstant.StandardNullableVarcharField(description="WhatsApp")
    telegram: DTOConstant.StandardNullableVarcharField(description="Telegram")
    instagram: DTOConstant.StandardNullableVarcharField(description="Instagram")
    tik_tok: DTOConstant.StandardNullableVarcharField(description="TikTok")
    site: DTOConstant.StandardNullableVarcharField(description="Сайт")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class AcademyWithRelationsRDTO(AcademyRDTO):
    image: FileRDTO | None = None
    city: CityRDTO | None = None

    class Config:
        from_attributes = True


class AcademyUpdateDTO(BaseModel):
    """DTO для обновления академии - все поля опциональные"""
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID главного изображения академии") | None = None
    city_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID города") | None = None
    title_ru: DTOConstant.StandardVarcharField(description="Название академии на русском") | None = None
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название академии на казахском") | None = None
    title_en: DTOConstant.StandardNullableVarcharField(description="Название академии на английском") | None = None
    description_ru: DTOConstant.StandardNullableTextField(description="Описание академии на русском") | None = None
    description_kk: DTOConstant.StandardNullableTextField(description="Описание академии на казахском") | None = None
    description_en: DTOConstant.StandardNullableTextField(description="Описание академии на английском") | None = None
    address_ru: DTOConstant.StandardNullableVarcharField(description="Адрес на русском") | None = None
    address_kk: DTOConstant.StandardNullableVarcharField(description="Адрес на казахском") | None = None
    address_en: DTOConstant.StandardNullableVarcharField(description="Адрес на английском") | None = None
    working_time: DTOConstant.StandardJSONField(description="Рабочее время в формате JSON") | None = None
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности академии") | None = None
    gender: DTOConstant.StandardTinyIntegerField(description="Пол: 0-оба, 1-мужской, 2-женский") | None = None
    min_age: DTOConstant.StandardIntegerField(description="Минимальный возраст") | None = None
    max_age: DTOConstant.StandardIntegerField(description="Максимальный возраст") | None = None
    average_price: DTOConstant.StandardNullableDecimalField(description="Средняя цена") | None = None
    average_training_time_in_minute: DTOConstant.StandardNullableIntegerField(description="Среднее время тренировки в минутах") | None = None
    phone: DTOConstant.StandardNullableVarcharField(description="Телефон") | None = None
    additional_phone: DTOConstant.StandardNullableVarcharField(description="Дополнительный телефон") | None = None
    email: DTOConstant.StandardNullableVarcharField(description="Email") | None = None
    whatsapp: DTOConstant.StandardNullableVarcharField(description="WhatsApp") | None = None
    telegram: DTOConstant.StandardNullableVarcharField(description="Telegram") | None = None
    instagram: DTOConstant.StandardNullableVarcharField(description="Instagram") | None = None
    tik_tok: DTOConstant.StandardNullableVarcharField(description="TikTok") | None = None
    site: DTOConstant.StandardNullableVarcharField(description="Сайт") | None = None

    class Config:
        from_attributes = True