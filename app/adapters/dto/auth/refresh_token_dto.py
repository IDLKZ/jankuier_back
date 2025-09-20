from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class RefreshTokenDTO(BaseModel):
    """
    DTO для запроса обновления токенов.

    Атрибуты:
        refresh_token (str): Refresh token для обновления токенов доступа.
    """

    refresh_token: DTOConstant.StandardTextField(
        description="Refresh token для обновления токенов доступа"
    )

    class Config:
        from_attributes = True