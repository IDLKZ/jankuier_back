from pydantic import BaseModel

from app.adapters.dto.permission.permission_dto import PermissionRDTO
from app.adapters.dto.role.role_dto import RoleRDTO
from app.shared.dto_constants import DTOConstant


class RolePermissionDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class RolePermissionCDTO(BaseModel):
    role_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID роли")
    permission_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID разрешения"
    )

    class Config:
        from_attributes = True


class RolePermissionRDTO(RolePermissionDTO):
    role_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID роли")
    permission_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID разрешения"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class RolePermissionWithRelationsRDTO(RolePermissionRDTO):
    role:RoleRDTO|None = None
    permission:PermissionRDTO|None = None
    class Config:
        from_attributes = True
