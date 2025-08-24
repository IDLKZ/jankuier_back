from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class SotaTokenDTO(BaseModel):
    refresh:DTOConstant.StandardNullableTextField(description="Refresh токен")
    access:DTOConstant.StandardTextField(description="Access токен")
    multi_token:DTOConstant.StandardNullableTextField(description="Multi токен")

    class Config:
        from_attributes = True