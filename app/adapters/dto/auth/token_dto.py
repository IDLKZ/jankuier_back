from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class BearerTokenDTO(BaseModel):
    """
    DTO для передачи токенов аутентификации.

    Атрибуты:
        access_token (str): Токен доступа для аутентифицированных запросов.
        refresh_token (str | None): Обновляемый токен для продления сессии.
    """

    access_token: DTOConstant.StandardTextField(
        description="Токен доступа для аутентифицированных запросов"
    )
    refresh_token: DTOConstant.StandardNullableTextField(
        description="Обновляемый токен для продления сессии"
    )

    class Config:
        from_attributes = True
