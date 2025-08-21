from pydantic import BaseModel
from app.adapters.dto.academy.academy_dto import AcademyRDTO
from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.pagination_dto import BasePageModel
from app.shared.dto_constants import DTOConstant


class AcademyGroupDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class AcademyGroupCDTO(BaseModel):
    academy_id: DTOConstant.StandardUnsignedIntegerField(description="ID академии")
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID изображения группы")
    name: DTOConstant.StandardVarcharField(description="Название группы")
    description_ru: DTOConstant.StandardNullableTextField(description="Описание группы на русском")
    description_kk: DTOConstant.StandardNullableTextField(description="Описание группы на казахском")
    description_en: DTOConstant.StandardNullableTextField(description="Описание группы на английском")
    value: DTOConstant.StandardUniqueValueField(description="Уникальное значение группы")
    min_age: DTOConstant.StandardIntegerField(description="Минимальный возраст")
    max_age: DTOConstant.StandardIntegerField(description="Максимальный возраст")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности группы")
    is_recruiting: DTOConstant.StandardBooleanFalseField(description="Идет набор в группу")
    gender: DTOConstant.StandardTinyIntegerField(description="Пол: 0-оба, 1-мужской, 2-женский")
    booked_space: DTOConstant.StandardIntegerDefaultZeroField(description="Занятых мест")
    free_space: DTOConstant.StandardIntegerDefaultZeroField(description="Свободных мест")
    price: DTOConstant.StandardNullableDecimalField(description="Цена")
    price_per_ru: DTOConstant.StandardNullableVarcharField(description="Описание цены на русском")
    price_per_kk: DTOConstant.StandardNullableVarcharField(description="Описание цены на казахском")
    price_per_en: DTOConstant.StandardNullableVarcharField(description="Описание цены на английском")
    average_training_time_in_minute: DTOConstant.StandardNullableIntegerField(description="Среднее время тренировки в минутах")

    class Config:
        from_attributes = True


class AcademyGroupRDTO(AcademyGroupDTO):
    academy_id: DTOConstant.StandardUnsignedIntegerField(description="ID академии")
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID изображения группы")
    name: DTOConstant.StandardVarcharField(description="Название группы")
    description_ru: DTOConstant.StandardNullableTextField(description="Описание группы на русском")
    description_kk: DTOConstant.StandardNullableTextField(description="Описание группы на казахском")
    description_en: DTOConstant.StandardNullableTextField(description="Описание группы на английском")
    value: DTOConstant.StandardUniqueValueField(description="Уникальное значение группы")
    min_age: DTOConstant.StandardIntegerField(description="Минимальный возраст")
    max_age: DTOConstant.StandardIntegerField(description="Максимальный возраст")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности группы")
    is_recruiting: DTOConstant.StandardBooleanFalseField(description="Идет набор в группу")
    gender: DTOConstant.StandardTinyIntegerField(description="Пол: 0-оба, 1-мужской, 2-женский")
    booked_space: DTOConstant.StandardIntegerDefaultZeroField(description="Занятых мест")
    free_space: DTOConstant.StandardIntegerDefaultZeroField(description="Свободных мест")
    price: DTOConstant.StandardNullableDecimalField(description="Цена")
    price_per_ru: DTOConstant.StandardNullableVarcharField(description="Описание цены на русском")
    price_per_kk: DTOConstant.StandardNullableVarcharField(description="Описание цены на казахском")
    price_per_en: DTOConstant.StandardNullableVarcharField(description="Описание цены на английском")
    average_training_time_in_minute: DTOConstant.StandardNullableIntegerField(description="Среднее время тренировки в минутах")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class AcademyGroupWithRelationsRDTO(AcademyGroupRDTO):
    academy: AcademyRDTO | None = None
    image: FileRDTO | None = None

    class Config:
        from_attributes = True


class AcademyGroupUpdateDTO(BaseModel):
    """DTO для обновления группы академии - все поля опциональные"""
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID изображения группы") | None = None
    name: DTOConstant.StandardVarcharField(description="Название группы") | None = None
    description_ru: DTOConstant.StandardNullableTextField(description="Описание группы на русском") | None = None
    description_kk: DTOConstant.StandardNullableTextField(description="Описание группы на казахском") | None = None
    description_en: DTOConstant.StandardNullableTextField(description="Описание группы на английском") | None = None
    min_age: DTOConstant.StandardIntegerField(description="Минимальный возраст") | None = None
    max_age: DTOConstant.StandardIntegerField(description="Максимальный возраст") | None = None
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности группы") | None = None
    is_recruiting: DTOConstant.StandardBooleanFalseField(description="Идет набор в группу") | None = None
    gender: DTOConstant.StandardTinyIntegerField(description="Пол: 0-оба, 1-мужской, 2-женский") | None = None
    booked_space: DTOConstant.StandardIntegerDefaultZeroField(description="Занятых мест") | None = None
    free_space: DTOConstant.StandardIntegerDefaultZeroField(description="Свободных мест") | None = None
    price: DTOConstant.StandardNullableDecimalField(description="Цена") | None = None
    price_per_ru: DTOConstant.StandardNullableVarcharField(description="Описание цены на русском") | None = None
    price_per_kk: DTOConstant.StandardNullableVarcharField(description="Описание цены на казахском") | None = None
    price_per_en: DTOConstant.StandardNullableVarcharField(description="Описание цены на английском") | None = None
    average_training_time_in_minute: DTOConstant.StandardNullableIntegerField(description="Среднее время тренировки в минутах") | None = None

    class Config:
        from_attributes = True


class PaginationAcademyGroupRDTO(BasePageModel):
    items: list[AcademyGroupRDTO]


class PaginationAcademyGroupWithRelationsRDTO(BasePageModel):
    items: list[AcademyGroupWithRelationsRDTO]