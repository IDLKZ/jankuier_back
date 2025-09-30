from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class BookingFieldPartyStatusDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class BookingFieldPartyStatusCDTO(BaseModel):
    """
    DTO для создания/обновления статуса бронирования площадки.
    """
    previous_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID предыдущего статуса"
    )
    next_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID следующего статуса"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение статуса"
    )
    title_ru: DTOConstant.StandardVarcharField(
        description="Название статуса на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название статуса на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название статуса на английском"
    )
    is_first: DTOConstant.StandardBooleanFalseField(
        description="Является ли первым статусом"
    )
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности")
    is_last: DTOConstant.StandardBooleanFalseField(
        description="Является ли последним статусом"
    )
    previous_allowed_values: DTOConstant.StandardNullableStringArrayField(
    )
    next_allowed_values: DTOConstant.StandardNullableStringArrayField(
    )

    class Config:
        from_attributes = True


class BookingFieldPartyStatusRDTO(BookingFieldPartyStatusDTO):
    """
    DTO для чтения статуса бронирования площадки.
    """
    previous_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID предыдущего статуса"
    )
    next_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID следующего статуса"
    )
    title_ru: DTOConstant.StandardVarcharField(
        description="Название статуса на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название статуса на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название статуса на английском"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение статуса"
    )
    is_first: DTOConstant.StandardBooleanFalseField(
        description="Является ли первым статусом"
    )
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности")
    is_last: DTOConstant.StandardBooleanFalseField(
        description="Является ли последним статусом"
    )
    previous_allowed_values: DTOConstant.StandardNullableStringArrayField(
    )
    next_allowed_values: DTOConstant.StandardNullableStringArrayField(
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class BookingFieldPartyStatusWithRelationsRDTO(BookingFieldPartyStatusRDTO):
    """
    DTO для чтения статуса бронирования площадки с relationships.
    """
    previous_status: "BookingFieldPartyStatusRDTO | None" = None
    next_status: "BookingFieldPartyStatusRDTO | None" = None

    class Config:
        from_attributes = True