from pydantic import BaseModel

from app.adapters.dto.notification.notification_dto import NotificationRDTO
from app.shared.dto_constants import DTOConstant


class ReadNotificationDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class ReadNotificationCDTO(BaseModel):
    notification_id: DTOConstant.StandardIntegerField(description="ID уведомления")
    user_id: DTOConstant.StandardIntegerField(description="ID пользователя")

    class Config:
        from_attributes = True


class ReadNotificationRDTO(ReadNotificationDTO):
    notification_id: DTOConstant.StandardIntegerField(description="ID уведомления")
    user_id: DTOConstant.StandardIntegerField(description="ID пользователя")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class ReadNotificationWithRelationsRDTO(ReadNotificationRDTO):
    notification: NotificationRDTO | None = None

    class Config:
        from_attributes = True
