from pydantic import BaseModel

from app.adapters.dto.topic_notification.topic_notification_dto import (
    TopicNotificationRDTO,
)
from app.shared.dto_constants import DTOConstant


class NotificationDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class NotificationCDTO(BaseModel):
    topic_id: DTOConstant.StandardIntegerField(description="ID топика уведомления")
    user_id: DTOConstant.StandardNullableIntegerField(
        description="ID пользователя (для персональных уведомлений)"
    )
    topics: DTOConstant.StandardNullableVarcharField(
        description="Список топиков через запятую для массовой рассылки"
    )
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Активно ли уведомление"
    )
    title_ru: DTOConstant.StandardVarcharField(
        description="Заголовок уведомления на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Заголовок уведомления на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Заголовок уведомления на английском"
    )
    description_ru: DTOConstant.StandardTextField(
        description="Описание уведомления на русском"
    )
    description_kk: DTOConstant.StandardNullableTextField(
        description="Описание уведомления на казахском"
    )
    description_en: DTOConstant.StandardNullableTextField(
        description="Описание уведомления на английском"
    )
    action_url: DTOConstant.StandardNullableVarcharField(
        description="Внешняя ссылка для перехода"
    )
    inner_action_url: DTOConstant.StandardNullableVarcharField(
        description="Внутренняя ссылка приложения"
    )

    class Config:
        from_attributes = True


class NotificationRDTO(NotificationDTO):
    topic_id: DTOConstant.StandardIntegerField(description="ID топика уведомления")
    user_id: DTOConstant.StandardNullableIntegerField(
        description="ID пользователя (для персональных уведомлений)"
    )
    topics: DTOConstant.StandardNullableVarcharField(
        description="Список топиков через запятую для массовой рассылки"
    )
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Активно ли уведомление"
    )
    title_ru: DTOConstant.StandardVarcharField(
        description="Заголовок уведомления на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Заголовок уведомления на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Заголовок уведомления на английском"
    )
    description_ru: DTOConstant.StandardTextField(
        description="Описание уведомления на русском"
    )
    description_kk: DTOConstant.StandardNullableTextField(
        description="Описание уведомления на казахском"
    )
    description_en: DTOConstant.StandardNullableTextField(
        description="Описание уведомления на английском"
    )
    action_url: DTOConstant.StandardNullableVarcharField(
        description="Внешняя ссылка для перехода"
    )
    inner_action_url: DTOConstant.StandardNullableVarcharField(
        description="Внутренняя ссылка приложения"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class NotificationWithRelationsRDTO(NotificationRDTO):
    topic: TopicNotificationRDTO | None = None

    class Config:
        from_attributes = True
