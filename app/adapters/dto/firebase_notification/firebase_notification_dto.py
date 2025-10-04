from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class FirebaseNotificationDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True

class FirebaseNotificationClientCDTO(BaseModel):
    token: DTOConstant.StandardTextField(description="Firebase токен устройства")
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Активен ли токен"
    )

class FirebaseNotificationCDTO(BaseModel):
    user_id: DTOConstant.StandardIntegerField(description="ID пользователя")
    token: DTOConstant.StandardTextField(description="Firebase токен устройства")
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Активен ли токен"
    )

    class Config:
        from_attributes = True


class FirebaseNotificationRDTO(FirebaseNotificationDTO):
    user_id: DTOConstant.StandardIntegerField(description="ID пользователя")
    token: DTOConstant.StandardTextField(description="Firebase токен устройства")
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Активен ли токен"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class FirebaseNotificationWithRelationsRDTO(FirebaseNotificationRDTO):
    class Config:
        from_attributes = True
