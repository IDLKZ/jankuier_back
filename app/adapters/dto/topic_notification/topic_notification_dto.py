from pydantic import BaseModel

from app.adapters.dto.file.file_dto import FileRDTO
from app.shared.dto_constants import DTOConstant


class TopicNotificationDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class TopicNotificationCDTO(BaseModel):
    image_id: DTOConstant.StandardNullableIntegerField(
        description="ID изображения топика уведомления"
    )
    title_ru: DTOConstant.StandardVarcharField(
        description="Название топика на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название топика на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название топика на английском"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение топика"
    )

    class Config:
        from_attributes = True


class TopicNotificationRDTO(TopicNotificationDTO):
    image_id: DTOConstant.StandardNullableIntegerField(
        description="ID изображения топика уведомления"
    )
    title_ru: DTOConstant.StandardVarcharField(
        description="Название топика на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название топика на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название топика на английском"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение топика"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class TopicNotificationWithRelationsRDTO(TopicNotificationRDTO):
    image: FileRDTO | None = None

    class Config:
        from_attributes = True
